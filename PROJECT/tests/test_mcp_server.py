import pytest
from fastmcp import FastMCP
from unittest.mock import patch, MagicMock
from main import index_folder, ask_question, find_relevant_docs, summarize_document, index_status
import os
import tempfile
import asyncio

def test_mcp_server_creation():
    """Test creating the MCP server"""
    from main import mcp
    assert mcp is not None
    assert isinstance(mcp, FastMCP)

def test_index_folder_tool():
    """Test the index_folder tool"""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_files = {
            "doc1.md": "# Document 1\n\nThis is the first test document.",
            "doc2.txt": "This is the second test document.",
            "doc3.py": "def function1():\n    pass\n\nclass Class1:\n    pass"
        }

        for filename, content in test_files.items():
            with open(os.path.join(temp_dir, filename), "w") as f:
                f.write(content)

        # Mock the document loader and vector store
        with patch('main.load_document') as mock_load_document, \
             patch('main.vector_store') as mock_vector_store:

            # Mock the load_document function to return fake documents
            mock_load_document.return_value = [
                MagicMock(page_content="Test content", metadata={"source": "test"})
            ]

            # Mock the vector store add_documents method
            mock_vector_store.add_documents.return_value = {
                "added_count": 1,
                "total_count": 1
            }

            # Call the index_folder function
            result = asyncio.run(index_folder(temp_dir))

            # Assertions
            assert result is not None
            assert "status" in result
            assert "message" in result
            assert "indexed_files" in result
            assert "total_documents" in result
            assert result["status"] == "success"
            assert result["indexed_files"] >= 0
            assert result["total_documents"] >= 0

            # Verify that load_document was called for each file
            assert mock_load_document.call_count >= 3

            # Verify that vector_store.add_documents was called
            assert mock_vector_store.add_documents.call_count >= 3

def test_ask_question_tool():
    """Test the ask_question tool"""
    # Mock the RAG pipeline
    with patch('main.rag_graph') as mock_rag_graph:

        # Mock the final state that would be returned by the RAG pipeline
        mock_final_state = MagicMock()
        mock_final_state.generation = "This is a test answer"
        mock_final_state.is_grounded = True
        mock_final_state.graded_documents = [
            MagicMock(metadata={"source": "test_doc1.txt"}),
            MagicMock(metadata={"source": "test_doc2.txt"})
        ]

        # Mock the RAG graph invoke method to return our mock state
        mock_rag_graph.invoke.return_value = mock_final_state

        # Call the ask_question function
        result = asyncio.run(ask_question("What is this?"))

        # Assertions
        assert result is not None
        assert "answer" in result
        assert "sources" in result
        assert "is_grounded" in result
        assert result["answer"] == "This is a test answer"
        assert result["is_grounded"] == True
        assert len(result["sources"]) == 2

        # Verify that rag_graph.invoke was called
        assert mock_rag_graph.invoke.call_count == 1

def test_find_relevant_docs_tool():
    """Test the find_relevant_docs tool"""
    # Mock the vector store search method
    with patch('main.vector_store') as mock_vector_store:

        # Mock documents that would be returned by the search
        mock_docs = [
            MagicMock(page_content="This is document 1", metadata={"source": "doc1.txt"}),
            MagicMock(page_content="This is document 2", metadata={"source": "doc2.txt"}),
            MagicMock(page_content="This is document 3", metadata={"source": "doc3.txt"})
        ]

        # Mock the vector store search method to return our mock documents
        mock_vector_store.search.return_value = mock_docs

        # Call the find_relevant_docs function
        result = asyncio.run(find_relevant_docs("test query", 3))

        # Assertions
        assert result is not None
        assert "documents" in result
        assert "query" in result
        assert "count" in result
        assert result["query"] == "test query"
        assert result["count"] == 3
        assert len(result["documents"]) == 3

        # Verify document structure
        for doc in result["documents"]:
            assert "content" in doc
            assert "metadata" in doc

        # Verify that vector_store.search was called with correct parameters
        mock_vector_store.search.assert_called_once_with("test query", n_results=3)

def test_summarize_document_tool():
    """Test the summarize_document tool"""
    # Mock the document loader and ollama
    with patch('main.load_document') as mock_load_document, \
         patch('main.ollama') as mock_ollama:

        # Mock documents that would be loaded
        mock_docs = [
            MagicMock(page_content="This is the content of the document. " * 100),
            MagicMock(page_content="This is more content. " * 50)
        ]

        # Mock the load_document function to return our mock documents
        mock_load_document.return_value = mock_docs

        # Mock the ollama response
        mock_ollama.generate.return_value = {
            "response": "This is a test summary of the document."
        }

        # Call the summarize_document function
        result = asyncio.run(summarize_document("/test/path/test_doc.txt"))

        # Assertions
        assert result is not None
        assert "summary" in result
        assert "file_path" in result
        assert "chunk_count" in result
        assert result["file_path"] == "/test/path/test_doc.txt"
        assert result["chunk_count"] == 2
        assert "This is a test summary" in result["summary"]

        # Verify that load_document was called
        mock_load_document.assert_called_once_with("/test/path/test_doc.txt")

        # Verify that ollama.generate was called
        assert mock_ollama.generate.call_count == 1

def test_index_status_tool():
    """Test the index_status tool"""
    # Mock the vector store get_stats method
    with patch('main.vector_store') as mock_vector_store:
        # Mock the get_stats method to return fake statistics
        mock_vector_store.get_stats.return_value = {
            "file_count": 5,
            "chunk_count": 12
        }

        # Call the index_status function
        result = asyncio.run(index_status())

        # Assertions
        assert result is not None
        assert "file_count" in result
        assert "chunk_count" in result
        assert result["file_count"] == 5
        assert result["chunk_count"] == 12

        # Verify that get_stats was called
        assert mock_vector_store.get_stats.call_count == 1