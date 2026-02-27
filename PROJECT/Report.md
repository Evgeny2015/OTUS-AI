# Отчет

## Install chromadb

> Use python 3.12 ONLY!!!
(python 3.14 has conflicts with current pydantic version)

For Windows the pymanager used to install different python version
```sh
# install python 3.12.10
py -3.12 -m venv .env
```

## ollama

* used qwen2.5-coder:1.5b

## sample docs
Used https://huggingface.co/datasets/databricks/databricks-dolly-15k cuted to 3000 lines
Execution time for index_folder: 134.2469 seconds

```
Indexing file ./sample_docs\databricks-dolly-15k.jsonl with 3000 chunks
Added 3000 documents to the vector store
Total documents in the vector store: 3000
Execution time for index_folder: 134.2469 seconds
Vector store has 3000 documents
```

