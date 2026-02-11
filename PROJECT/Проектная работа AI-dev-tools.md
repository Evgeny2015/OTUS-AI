# RAG Knowledge Base — MCP-сервер с локальной LLM и LangGraph

MCP-сервер, который превращает локальную папку с документами в поисковую базу знаний. Разработчик подключает сервер к IDE, индексирует документы (проектная документация, внутренняя wiki, заметки) и задаёт вопросы — AI в IDE получает ответы, основанные на содержимом файлов.

Внутри сервера — RAG-пайплайн на LangGraph с локальной LLM через Ollama (без платных API).

## Результаты

* MCP-сервер с 5 инструментами (см. ниже)
* LangGraph-граф с условными переходами и retry-циклами (Corrective RAG)
* Docker Compose: сервер \+ Ollama \+ модель — запуск одной командой
  (допустимо использовать локальную Ollama без Docker по дефолтному адресу)
* Набор демо-документов и тесты


## Технологии

* Python, FastMCP
* LangGraph (оркестрация), LangChain (документ-лоадеры, сплиттеры, векторный стор)
* Ollama \+ локальная маленькая LLM
  (например, Phi-3-mini (3.8B) или Qwen2.5-3B)
* ChromaDB — векторное хранилище (in-process, без отдельного сервера), дефолтная модель эмбеддингов
* Docker, Docker Compose


# MCP-инструменты (5)

| Инструмент | Вход | Что делает | Нужна LLM? |
| ----- | ----- | ----- | ----- |
| `index_folder` | путь к папке, glob-паттерн | Сканирует файлы, разбивает на чанки, создаёт эмбеддинги, сохраняет в ChromaDB | Только эмбеддинги |
| `ask_question` | строка-вопрос | Запускает полный RAG-пайплайн (LangGraph) | Да — локальная LLM |
| `find_relevant_docs` | запрос, top\_k | Возвращает ранжированные чанки без генерации ответа | Только эмбеддинги |
| `summarize_document` | путь к файлу | Разбивает документ на чанки, генерирует саммари | Да — локальная LLM |
| `index_status` | — | Статистика: количество файлов, чанков, время последней индексации | Нет |


# Поддерживаемые форматы документов

* `.md`, `.txt`, `.rst` — текстовые файлы
* `.py`, `.js`, `.ts` — код (разбивка по функциям)
* `.json`, `.yaml` — структурированные данные



# LangGraph-граф (Corrective RAG)

User Query → Rewrite Query → Retrieve (vector search)
 → Grade Chunks (relevant? yes/no)
   → enough relevant → Generate Answer → Hallucination Check
                          → grounded → Return answer \+ sources
                          → not grounded → Regenerate (max 1 retry)
   → too few relevant → Broaden Query → Retrieve (max 2 loops)

# LangGraph State

class RAGState(TypedDict):
   question: str
   rewritten\_query: str
   documents: list\[Document\]
   graded\_documents: list\[Document\]
   generation: str
   sources: list\[str\]
   retry\_count: int
   is\_grounded: bool

# Проверка преподавателем

docker compose up   \# поднимает сервер \+ Ollama \+ скачивает модель
\# подключить MCP-сервер в IDE или MCP Inspector
\# index\_folder("./sample\_docs") → ask\_question("Как оформлять docstrings?")

# Дополнительное задание (необязательное)

* Поддержка внешней модели эмбеддингов через Ollama (например, `nomic-embed-text`) вместо дефолтной ChromaDB. Переключение через конфиг — без изменения остального кода.
* Поддержка `.pdf` — парсинг PDF-документов (через PyPDFLoader или аналог), индексация наравне с текстовыми файлами.


# Процесс сдачи

1. Репозиторий — студент предоставляет ссылку на GitHub-репозиторий.
2. Запуск — преподаватель выполняет:
   git clone \<repo\> && cd \<repo\>
   docker compose up
3. Проверка инструментов — через MCP Inspector или подключение к IDE:
   * `index_status()` → пустой индекс
   * `index_folder("./sample_docs")` → индексация демо-документов
   * `index_status()` → статистика (количество файлов, чанков)
   * `ask_question("...")` → ответ с указанием источников
   * `find_relevant_docs("...")` → список релевантных чанков
   * `summarize_document("./sample_docs/api_reference.md")` → саммари
4. Тесты — преподаватель запускает:
   docker compose exec server pytest
5. Код-ревью — просмотр структуры проекта, графа LangGraph, тестов.
6. Демо (5 минут) — студент показывает работу сервера в IDE, объясняет архитектуру графа.


# Критерии оценки

* MCP-сервер — все 5 инструментов работают, корректные входы/выходы, обработка ошибок.
* LangGraph-граф — Corrective RAG реализован: rewrite → retrieve → grade → generate → hallucination check. Условные переходы и retry-циклы работают.
* Индексация документов — поддержка всех обязательных форматов, корректная разбивка на чанки, метаданные (источник, позиция) сохраняются.
* Тесты — не менее 10 тестов: unit-тесты графа с mock LLM, тесты индексера, e2e-тест MCP-инструментов.
* Инфраструктура — Docker Compose запускается одной командой, CI pipeline (lint \+ тесты), seed-документы в комплекте.
* Качество кода — читаемость, структура проекта, конфигурация вынесена, отсутствие хардкода.
* Документация — README: архитектура, инструкция по запуску, примеры использования.

