# Архитектура проекта

## Обзор

RAG Knowledge Base — это MCP-сервер, который превращает локальную папку с документами в поисковую базу знаний. Сервер позволяет индексировать документы различных форматов и задавать вопросы к ним с помощью локальной LLM через Ollama.

## Архитектура системы

```mermaid
graph TD
    A[Пользователь/IDE] --> B[MCP Server]
    B --> C[RAG Pipeline]
    C --> D[Document Loader]
    C --> E[Vector Store]
    C --> F[Ollama LLM]
    E --> G[ChromaDB]
    H[Документы] --> D
    I[Запросы] --> C

    style B fill:#4CAF50,stroke:#388E3C
    style C fill:#2196F3,stroke:#0D47A1
    style D fill:#FF9800,stroke:#E65100
    style E fill:#9C27B0,stroke:#4A148C
    style F fill:#F44336,stroke:#B71C1C
    style G fill:#9E9E9E,stroke:#212121
```

## Основные компоненты

### 1. MCP Server (main.py)
- **Назначение**: Точка входа в приложение, предоставляет API для взаимодействия с внешними системами
- **Функции**:
  - Экспонирование инструментов для индексации документов и ответов на вопросы
  - Обработка запросов от IDE или других клиентов
  - Управление жизненным циклом приложения

### 2. RAG Pipeline (rag_pipeline.py)
- **Назначение**: Реализация пайплайна Retrieval-Augmented Generation с коррекцией
- **Компоненты**:
  - **Rewrite Query**: Переформулирование запроса для улучшения поиска
  - **Retrieve**: Поиск релевантных документов в векторной базе
  - **Grade Documents**: Оценка релевантности найденных документов
  - **Generate Answer**: Генерация ответа на основе релевантных документов
  - **Hallucination Check**: Проверка достоверности сгенерированного ответа
  - **Broaden Query**: Расширение запроса при недостатке релевантных документов

### 3. Document Loader (document_loader.py)
- **Назначение**: Загрузка и предварительная обработка документов различных форматов
- **Поддерживаемые форматы**:
  - Текстовые файлы (.txt, .md, .rst)
  - Файлы кода (.py, .js, .ts) с разбивкой по функциям/классам
  - Структурированные данные (.json, .jsonl, .yaml)

### 4. Vector Store (vector_store.py)
- **Назначение**: Хранение и поиск векторных представлений документов
- **Реализация**: ChromaDB с персистентным хранением
- **Функции**:
  - Добавление документов с созданием эмбеддингов
  - Поиск похожих документов по векторному представлению
  - Получение статистики по индексированным документам

### 5. Ollama LLM
- **Назначение**: Локальная генерация текста для переформулирования запросов, оценки релевантности и генерации ответов
- **Модель**: По умолчанию используется qwen2.5:3b

## Поток данных

### Индексация документов
```mermaid
sequenceDiagram
    participant U as Пользователь
    participant M as MCP Server
    participant D as Document Loader
    participant V as Vector Store
    participant C as ChromaDB

    U->>M: index_folder(folder_path)
    M->>D: load_document(file_path)
    D-->>M: documents[]
    M->>V: add_documents(documents)
    V->>C: Сохранение эмбеддингов
    M-->>U: Статус индексации
```

### Обработка вопросов
```mermaid
sequenceDiagram
    participant U as Пользователь
    participant M as MCP Server
    participant R as RAG Pipeline
    participant V as Vector Store
    participant O as Ollama LLM
    participant C as ChromaDB

    U->>M: ask_question(question)
    M->>R: rag_graph.invoke(state)
    R->>O: Переформулирование запроса
    O-->>R: rewritten_query
    R->>V: search(rewritten_query)
    V->>C: Поиск похожих документов
    C-->>V: documents[]
    V-->>R: documents[]
    R->>O: Оценка релевантности
    O-->>R: graded_documents[]
    R->>O: Генерация ответа
    O-->>R: generation
    R->>O: Проверка достоверности
    O-->>R: is_grounded
    R-->>M: final_state
    M-->>U: answer, sources
```

## Docker конфигурация

### Сервисы
1. **ollama**: Контейнер с Ollama для запуска локальной LLM
2. **server**: Контейнер с MCP-сервером

### Порты
- 11434: Порт Ollama
- 8001: Порт MCP-сервера

## Инструменты MCP

| Инструмент | Назначение | Требуется LLM |
|------------|------------|---------------|
| `index_folder` | Индексация документов в папке | Только эмбеддинги |
| `ask_question` | Ответ на вопрос по индексированным документам | Да |
| `find_relevant_docs` | Поиск релевантных документов | Только эмбеддинги |
| `summarize_document` | Создание краткого содержания документа | Да |
| `index_status` | Получение статистики индекса | Нет |

## Технологический стек

- **Язык программирования**: Python 3.12
- **Фреймворки**: FastMCP, LangGraph, LangChain
- **Векторная база данных**: ChromaDB
- **LLM**: Ollama (qwen2.5:3b)
- **Контейнеризация**: Docker, Docker Compose
- **Тестирование**: Pytest

## Детализированная архитектура системы

```mermaid
graph LR
    A[Клиенты] --> B[MCP Server]
    B --> C[RAG Pipeline]

    subgraph "RAG Pipeline"
        C --> D[Query Rewriter]
        D --> E[Document Retriever]
        E --> F[Document Grader]
        F --> G[Answer Generator]
        G --> H[Hallucination Checker]
        F --> I[Broaden Query]
        I --> E
        H --> J[Retry Logic]
        J --> G
    end

    subgraph "Data Sources"
        K[Document Files] --> L[Document Loader]
        L --> M[Vector Store]
        N[Ollama LLM] --> O[LLM Interface]
    end

    subgraph "Storage"
        M --> P[ChromaDB]
    end

    C --> O
    E --> M
    F --> O
    G --> O
    H --> O
    I --> O
    D --> O

    style A fill:#4CAF50,stroke:#388E3C
    style B fill:#2196F3,stroke:#0D47A1
    style C fill:#FF9800,stroke:#E65100
    style M fill:#9C27B0,stroke:#4A148C
    style N fill:#F44336,stroke:#B71C1C
    style P fill:#9E9E9E,stroke:#212121
