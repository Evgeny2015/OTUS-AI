# RAG Knowledge Base — MCP-сервер с локальной LLM и LangGraph

MCP-сервер, который превращает локальную папку с документами в поисковую базу знаний. Разработчик подключает сервер к IDE, индексирует документы (проектная документация, внутренняя wiki, заметки) и задаёт вопросы — AI в IDE получает ответы, основанные на содержимом файлов.

Внутри сервера — RAG-пайплайн на LangGraph с локальной LLM через Ollama (без платных API).

## Архитектура

### Компоненты

1. **MCP Server**: Exposes five tools for document indexing and querying
2. **LangGraph Pipeline**: Implements a Corrective RAG workflow with query rewriting, document retrieval, grading, answer generation, and hallucination checking
3. **Document Loaders**: Support for various file formats including markdown, text, code files, and structured data
4. **Vector Store**: ChromaDB for storing document embeddings
5. **Local LLM**: Ollama integration for running models locally

### LangGraph-граф (Corrective RAG)

```
User Query → Rewrite Query → Retrieve (vector search)
 → Grade Chunks (relevant? yes/no)
   → enough relevant → Generate Answer → Hallucination Check
                          → grounded → Return answer + sources
                          → not grounded → Regenerate (max 1 retry)
   → too few relevant → Broaden Query → Retrieve (max 2 loops)
```

## Поддерживаемые форматы документов

- `.md`, `.txt`, `.rst` — текстовые файлы
- `.py`, `.js`, `.ts` — код (разбивка по функциям)
- `.json`, `.jsonl`, `.yaml` — структурированные данные

## Быстрый старт

1. Установите Docker и Docker Compose
2. Запустите сервер и Ollama:
   ```bash
   docker-compose up
   ```
3. Подключите MCP-сервер к вашей IDE или используйте MCP Inspector
4. Индексируйте документы:
   ```python
   index_folder("./sample_docs")
   ```
5. Задавайте вопросы:
   ```python
   ask_question("Как оформлять docstrings?")
   ```

## Инструменты MCP

| Инструмент | Вход | Что делает | Нужна LLM? |
| ----- | ----- | ----- | ----- |
| `index_folder` | путь к папке, glob-паттерн | Сканирует файлы, разбивает на чанки, создаёт эмбеддинги, сохраняет в ChromaDB | Только эмбеддинги |
| `ask_question` | строка-вопрос | Запускает полный RAG-пайплайн (LangGraph) | Да — локальная LLM |
| `find_relevant_docs` | запрос, top_k | Возвращает ранжированные чанки без генерации ответа | Только эмбеддинги |
| `summarize_document` | путь к файлу | Разбивает документ на чанки, генерирует саммари | Да — локальная LLM |
| `index_status` | — | Статистика: количество файлов, чанков, время последней индексации | Нет |

## Разработка

### Структура проекта

```
.
├── main.py                 # Точка входа MCP-сервера
├── rag_pipeline.py         # LangGraph RAG pipeline
├── document_loader.py     # Загрузчики документов
├── vector_store.py        # Интерфейс к ChromaDB
├── requirements.txt       # Зависимости Python
├── Dockerfile             # Docker-образ сервера
├── docker-compose.yml     # Docker Compose конфигурация
├── sample_docs/           # Демо-документы
└── tests/                # Тесты
```

### Запуск тестов

```bash
docker-compose exec server pytest
```