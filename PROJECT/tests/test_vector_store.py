import pytest
import tempfile
from langchain_core.documents import Document
from main import ask_question, index_folder, index_status
from vector_store import VectorStore, vectorStore
import os
import asyncio
import time

@pytest.fixture
def vector_store():
    """Create a temporary vector store for testing"""
    temp_dir = tempfile.mkdtemp()
    store = VectorStore(temp_dir)

    def cleanup():
        import shutil
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass  # Ignore cleanup errors on Windows

    import atexit
    atexit.register(cleanup)
    yield store
    cleanup()

def test_add_documents_basic(vector_store):
    """Test adding documents to the vector store"""
    documents = [
        Document(page_content="This is document 1", metadata={"source": "test1.txt"}),
        Document(page_content="This is document 2", metadata={"source": "test2.txt"})
    ]

    result = vector_store.add_documents(documents)
    assert result["added_count"] == 2
    assert result["total_count"] == 2

def test_search(vector_store):
    """Test searching for documents"""
    # Add some documents first
    documents = [
        Document(page_content="Python is a programming language", metadata={"source": "python.txt"}),
        Document(page_content="Java is also a programming language", metadata={"source": "java.txt"})
    ]
    vector_store.add_documents(documents)

    # Search for similar documents
    results = vector_store.search("programming language", n_results=2)
    assert len(results) == 2
    assert "programming language" in results[0].page_content.lower()

def test_get_stats(vector_store):
    """Test getting vector store statistics"""
    # Initially empty
    stats = vector_store.get_stats()
    assert stats["file_count"] == 0
    assert stats["chunk_count"] == 0

    # Add some documents
    documents = [
        Document(page_content="Document 1", metadata={"source": "test1.txt"}),
        Document(page_content="Document 2", metadata={"source": "test1.txt"}),  # Same source
        Document(page_content="Document 3", metadata={"source": "test2.txt"})
    ]
    vector_store.add_documents(documents)

    # Check stats again
    stats = vector_store.get_stats()
    assert stats["file_count"] == 2  # Two unique sources
    assert stats["chunk_count"] == 3  # Three chunks total

'''
def test_get_status():
    """Test getting vector store status"""
    # Initially empty
    status = asyncio.run(index_status())
    print(status)


def test_reset():
    """Test resetting the vector store"""
    # Reset the store
    vectorStore.reset()

    # Check stats again
    stats = vectorStore.get_stats()
    assert stats["file_count"] == 0
    assert stats["chunk_count"] == 0

def test_add_documents_from_folder():
    """Test adding documents to the vector store from a folder"""

    # Run the async function
    start_time = time.time()
    asyncio.run(index_folder("./sample_docs"))
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time for index_folder: {execution_time:.4f} seconds")

    # Check stats again
    stats = asyncio.run(index_status())

    assert stats["file_count"] == 1  # We have one file in sample_docs
    assert stats["chunk_count"] >= 1  # Should have at least one chunk

def test_search_from_folder():
    """Test searching for documents from a folder"""
    # Search for similar documents
    results = vectorStore.search("What is a Pyhton?", n_results=2)

    print(results)


def test_ask_question():
    """Test asking a question"""
    # ask_question
    question = "Cobra language"
    answer = asyncio.run(ask_question(question))

    print(answer)
'''