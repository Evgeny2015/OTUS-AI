import pytest
from rag_pipeline import RAGState, create_rag_graph

def test_rag_state_creation():
    """Test creating a RAGState object"""
    state = RAGState(
        question="What is Python?",
        rewritten_query="Python programming language",
        documents=[],
        graded_documents=[],
        generation="",
        sources=[],
        retry_count=0,
        is_grounded=False
    )

    assert state.question == "What is Python?"
    assert state.rewritten_query == "Python programming language"
    assert state.retry_count == 0

def test_graph_creation():
    """Test creating the RAG graph"""
    graph = create_rag_graph()
    assert graph is not None

def test_rewrite_query_node():
    """Test the rewrite_query node"""
    from rag_pipeline import rewrite_query

    state = RAGState(
        question="What is Python?",
        rewritten_query="",
        documents=[],
        graded_documents=[],
        generation="",
        sources=[],
        retry_count=0,
        is_grounded=False
    )

    result = rewrite_query(state)
    assert "rewritten_query" in result
    # In the placeholder implementation, the rewritten query is the same as the original
    assert result["rewritten_query"] == state.question

def test_grade_documents_node():
    """Test the grade_documents node"""
    from rag_pipeline import grade_documents
    from langchain_core.documents import Document

    documents = [
        Document(page_content="Python is a programming language", metadata={"source": "python.txt"}),
        Document(page_content="Java is also a programming language", metadata={"source": "java.txt"})
    ]

    state = RAGState(
        question="What is Python?",
        rewritten_query="Python programming language",
        documents=documents,
        graded_documents=[],
        generation="",
        sources=[],
        retry_count=0,
        is_grounded=False
    )

    result = grade_documents(state)
    assert "graded_documents" in result
    # In the placeholder implementation, all documents are considered relevant
    assert len(result["graded_documents"]) == len(documents)

def test_hallucination_check_node():
    """Test the hallucination_check node"""
    from rag_pipeline import check_hallucination

    state = RAGState(
        question="What is Python?",
        rewritten_query="Python programming language",
        documents=[],
        graded_documents=[],
        generation="Python is a programming language",
        sources=[],
        retry_count=0,
        is_grounded=False
    )

    result = check_hallucination(state)
    assert "is_grounded" in result
    # With no documents, the answer cannot be grounded
    assert result["is_grounded"] == False
