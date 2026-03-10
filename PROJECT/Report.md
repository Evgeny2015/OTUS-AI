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

* used qwen2.5:3b

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

## answer generation

> llama3.2:3b generate answer `Python.` for the prompt:

```
Answer the question based only on the provided context. If the answer cannot be determined from the context, say "I don't have enough information to answer that question."

    Question: What is a Pyhton?

    Context:
    {
  "instruction": "What is Python?",
  "context": "",
  "response": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation via the off-side rule.\n\nPython is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a \"batteries included\" language due to its comprehensive standard library.",
  "category": "open_qa"
}

{
  "instruction": "Which ones are programming languages, out of C, Java, Node.js, Python, HTML, BigData, Spark?",
  "context": "",
  "response": "Well, C, Java and Python are programming languages. \nWhile HTML is a language, it is a markup language and not a programming language. Node.js is actually a framework built on top of Javascript, so it can't be classified as a language. \nBigData is a broader term used for storing, processing and usage of large amounts of data. Spark is one of the most popular distributed data processing frameworks. Spark can be used from multiple languages.",
  "category": "classification"
}

    Answer:
```

Decision: using model qwen2.5:3b.

## test
Question: What is a Pyhton?

### qwen2.5:3b+RAG
```json
{"answer": "Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation via the off-side rule. Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented, and functional programming. It is often described as a \"batteries included\" language due to its comprehensive standard library.", "sources": ["./sample_docs\\databricks-dolly-15k.jsonl"], "is_grounded": true}
```

### qwen2.5:3b
```
Python is not a programming language; it's actually the name of a high-level, interpreted programming language. It was developed by Guido van Rossum
and first released in 1991. Python is known for its clear syntax which allows programmers to express concepts using less code than other languages.

Some key features of Python include:

- **Readability:** The syntax of Python encourages the use of indentation, making it very easy to read.
- **Versatility:** It can be used for web development (with frameworks like Django and Flask), scientific computing, data analysis and visualization,
artificial intelligence, machine learning, automation scripting, and more.
- **Ease of Use:** Python has a large standard library which makes developing applications easier.

Python is also supported by an extensive ecosystem of third-party libraries known as "pip" to install various modules for different functions.

If you meant something else by your question, please provide more context or ask another question!
```

## test

* appane fake article:
```
Cobra is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation via the off-side rule.\n\nCobra is statically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a \"batteries included\" language due to its comprehensive standard library.
```
* reindex vector DB

* Question: What is Cobra language?

* response:
```
{"instruction": "What is Cobra?", "context": "", "response": "Cobra is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation via the off-side rule.\n\nCobra is statically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a \"batteries included\" language due to its comprehensive standard library.", "category": "open_qa"}
```