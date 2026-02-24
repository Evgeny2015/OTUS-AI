import pytest
import os
from document_loader import load_document

def test_load_markdown():
    """Test loading a markdown document"""
    # Create a temporary markdown file
    content = """# Test Document

## Section 1
This is the first section.

## Section 2
This is the second section."""

    with open("test.md", "w") as f:
        f.write(content)

    try:
        documents = load_document("test.md")
        assert len(documents) >= 2
        assert "first section" in documents[1].page_content
        assert "second section" in documents[2].page_content
    finally:
        os.remove("test.md")

def test_load_text():
    """Test loading a text document"""
    # Create a temporary text file
    content = "This is a test document.\nIt has multiple lines.\nFor testing purposes."

    with open("test.txt", "w") as f:
        f.write(content)

    try:
        documents = load_document("test.txt")
        assert len(documents) >= 1
        assert "test document" in documents[0].page_content
    finally:
        os.remove("test.txt")

def test_load_python():
    """Test loading a Python document"""
    # Create a temporary Python file
    content = """def function1():
    pass

class Class1:
    def method1(self):
        pass"""

    with open("test.py", "w") as f:
        f.write(content)

    try:
        documents = load_document("test.py")
        assert len(documents) >= 2
        assert "function1" in documents[0].page_content
        assert "Class1" in documents[1].page_content
    finally:
        os.remove("test.py")

def test_load_json():
    """Test loading a JSON document"""
    # Create a temporary JSON file
    content = '{"key1": "value1", "key2": "value2"}'

    with open("test.json", "w") as f:
        f.write(content)

    try:
        documents = load_document("test.json")
        assert len(documents) == 1
        assert "key1" in documents[0].page_content
    finally:
        os.remove("test.json")

def test_load_yaml():
    """Test loading a YAML document"""
    # Create a temporary YAML file
    content = "key1: value1\nkey2: value2"

    with open("test.yaml", "w") as f:
        f.write(content)

    try:
        documents = load_document("test.yaml")
        assert len(documents) == 1
        assert "key1" in documents[0].page_content
    finally:
        os.remove("test.yaml")

def test_file_not_found():
    """Test loading a non-existent file"""
    with pytest.raises(FileNotFoundError):
        load_document("non_existent_file.txt")