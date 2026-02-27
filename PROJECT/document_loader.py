import os
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import yaml
import json

def load_document(file_path: str) -> List[Document]:
    """Load a document and split it into chunks"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine file type and load accordingly
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.md':
        return load_markdown(file_path)
    elif file_extension == '.txt':
        return load_text(file_path)
    elif file_extension == '.rst':
        return load_rst(file_path)
    elif file_extension == '.py':
        return load_python(file_path)
    elif file_extension == '.js':
        return load_javascript(file_path)
    elif file_extension == '.ts':
        return load_typescript(file_path)
    elif file_extension == '.json':
        return load_json(file_path)
    elif file_extension == '.jsonl':
        return load_jsonl(file_path)
    elif file_extension == '.yaml' or file_extension == '.yml':
        return load_yaml(file_path)
    else:
        # Default to text loading for unknown formats
        return load_text(file_path)

def load_markdown(file_path: str) -> List[Document]:
    """Load a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into sections by headers
    sections = content.split('\n## ')
    documents = []

    for i, section in enumerate(sections):
        if i == 0 and not section.startswith('##'):
            # This is the title section
            doc = Document(
                page_content=section,
                metadata={"source": file_path, "section": "title"}
            )
        else:
            # This is a header section
            lines = section.split('\n')
            header = lines[0]
            content = '\n'.join(lines[1:])
            doc = Document(
                page_content=content,
                metadata={"source": file_path, "section": header}
            )
        documents.append(doc)

    return documents

def load_text(file_path: str) -> List[Document]:
    """Load a text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use recursive character splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    docs = splitter.create_documents([content])
    for doc in docs:
        doc.metadata["source"] = file_path

    return docs

def load_rst(file_path: str) -> List[Document]:
    """Load a reStructuredText file"""
    # For now, treat as regular text
    return load_text(file_path)

def load_python(file_path: str) -> List[Document]:
    """Load a Python file, splitting by functions and classes"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple approach: split by def and class keywords
    lines = content.split('\n')
    documents = []
    current_chunk = []
    current_header = "file_start"

    for line in lines:
        if line.startswith('def ') or line.startswith('class '):
            # Save previous chunk
            if current_chunk:
                doc_content = '\n'.join(current_chunk)
                doc = Document(
                    page_content=doc_content,
                    metadata={"source": file_path, "section": current_header}
                )
                documents.append(doc)

            # Start new chunk
            current_chunk = [line]
            current_header = line.split('(')[0].strip()
        else:
            current_chunk.append(line)

    # Don't forget the last chunk
    if current_chunk:
        doc_content = '\n'.join(current_chunk)
        doc = Document(
            page_content=doc_content,
            metadata={"source": file_path, "section": current_header}
        )
        documents.append(doc)

    return documents

def load_javascript(file_path: str) -> List[Document]:
    """Load a JavaScript file"""
    # For now, treat as regular text
    return load_text(file_path)

def load_typescript(file_path: str) -> List[Document]:
    """Load a TypeScript file"""
    # For now, treat as regular text
    return load_text(file_path)

def load_json(file_path: str) -> List[Document]:
    """Load a JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert to string and treat as text
    content = json.dumps(data, indent=2)
    doc = Document(
        page_content=content,
        metadata={"source": file_path, "type": "json"}
    )

    return [doc]

def load_yaml(file_path: str) -> List[Document]:
    """Load a YAML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Convert to string and treat as text
    content = yaml.dump(data, indent=2)
    doc = Document(
        page_content=content,
        metadata={"source": file_path, "type": "yaml"}
    )

    return [doc]

def load_jsonl(file_path: str) -> List[Document]:
    """Load a JSONL (JSON Lines) file"""
    documents = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
                # Convert to string and treat as text
                content = json.dumps(data, indent=2)
                doc = Document(
                    page_content=content,
                    metadata={"source": file_path, "type": "jsonl", "line": line_num}
                )
                documents.append(doc)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {line_num}: {e}")

    return documents