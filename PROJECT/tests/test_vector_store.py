import pytest
from langchain_core.documents import Document
from vector_store import VectorStore
import tempfile
import os

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

def test_add_documents(vector_store):
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