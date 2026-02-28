import os
import sys
import ollama
from vector_store import vectorStore
from typing import List, Dict, Any
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
import asyncio
from loguru import logger

# Set up logging
logger.add(sys.stderr, level="INFO")

#DEFAULT_OLLAMA_MODEL = "llama3.2:3b"
DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"

class RAGState(BaseModel):
    """State for the RAG pipeline"""
    question: str = Field(description="The original question")
    rewritten_query: str = Field(description="The rewritten query for search")
    documents: List[Document] = Field(description="Retrieved documents")
    graded_documents: List[Document] = Field(description="Graded documents")
    generation: str = Field(description="Generated answer")
    sources: List[str] = Field(description="Source documents")
    query_retry_count: int = Field(description="Number of retries for query")
    answer_retry_count: int = Field(description="Number of retries for answer")
    is_grounded: bool = Field(description="Whether the answer is grounded")

# Node functions
def rewrite_query(state: RAGState) -> Dict[str, Any]:
    """Rewrite the query to improve search results"""
    # Use an LLM to rewrite the query for better search results
    prompt = f"""Rewrite the following question to improve search results.
    Make it more specific and focused on finding relevant information.
    Original question: {state.question}
    """

    logger.info(f"Rewriting query for question: {state.question}")

    try:
        response = ollama.generate(
            model=DEFAULT_OLLAMA_MODEL,
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        rewritten_query = response['response'].strip()
        # If the LLM didn't generate a useful query, fall back to the original
        if not rewritten_query or len(rewritten_query) < 3:
            logger.warning("LLM didn't generate a useful query, falling back to original")
            rewritten_query = state.question

    except Exception as e:
        # If LLM fails, use the original query
        logger.exception("Error rewriting query", e)
        rewritten_query = state.question

    return {"rewritten_query": rewritten_query}

def retrieve_documents(state: RAGState) -> Dict[str, Any]:
    """Retrieve documents based on the query"""
    # Use the vector store to retrieve relevant documents
    logger.info(f"Retrieving documents for query: {state.rewritten_query}")
    try:
        documents = vectorStore.search(state.rewritten_query, n_results=3)
    except Exception as e:
        # If retrieval fails, return empty list
        documents = []
        logger.exception("Error retrieving documents", e)

    return {"documents": documents}

def grade_documents(state: RAGState) -> Dict[str, Any]:
    """Grade documents for relevance"""
    if not state.documents:
        logger.info("No documents to grade, returning empty list")
        return {"graded_documents": []}

    # Use an LLM to grade each document for relevance
    graded_documents = []

    for doc in state.documents:
        prompt = f"""Given the question and a document, determine if the document is relevant to answering the question.

        Question: {state.question}

        Document: {doc.page_content[:500]}...

        Is this document relevant to answering the question? Respond with only "yes" or "no"."""

        try:
            response = ollama.generate(
                model=DEFAULT_OLLAMA_MODEL,
                prompt=prompt,
                options={
                    "temperature": 0.0,  # Low temperature for consistent responses
                    "stop": ["\n"]
                }
            )
            answer = response['response'].strip().lower()

            # If the LLM says yes, include the document
            if "yes" in answer:
                graded_documents.append(doc)
        except Exception as e:
            # If LLM fails, include the document by default
            graded_documents.append(doc)
            logger.exception("Error grading document", e)

    return {"graded_documents": graded_documents}

def generate_answer(state: RAGState) -> Dict[str, Any]:
    """Generate an answer based on the documents"""
    logger.info(f"Generating answer for question: {state.question} with {len(state.graded_documents)} graded documents")

    if not state.graded_documents:
        logger.info("No graded documents available, returning default response")
        return {"generation": "I don't have enough information to answer that question."}

    # Combine the graded documents into context
    context = "\n\n".join([doc.page_content for doc in state.graded_documents[:5]])

    # Use an LLM to generate an answer based on the documents
    prompt = f"""Answer the question based only on the provided context. If the answer cannot be determined from the context, say "I don't have enough information to answer that question."

    Question: {state.question}

    Context:
    {context}

    Answer:"""

    try:
        response = ollama.generate(
            model=DEFAULT_OLLAMA_MODEL,
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        generation = response['response'].strip()
    except Exception as e:
        # If LLM fails, provide a fallback answer
        generation = "I'm sorry, but I'm having trouble generating an answer right now."
        logger.exception(f"Error generating answer", e)

    return {"generation": generation}

def check_hallucination(state: RAGState) -> Dict[str, Any]:
    """Check if the answer is grounded in the documents"""
    logger.info(f"Checking hallucination for answer: {state.generation[:50]}...")

    if not state.graded_documents or not state.generation:
        logger.info("No graded documents or generation available, returning not grounded")
        return {"is_grounded": False}

    # Combine the graded documents into context
    context = "\n\n".join([doc.page_content for doc in state.graded_documents[:5]])

    # Use an LLM to check if the answer is grounded in the documents
    prompt = f"""Determine if the following answer is grounded in the provided context.
    An answer is grounded if all the information in the answer can be derived from the context.

    Answer: {state.generation}

    Context:
    {context}

    Is the answer grounded in the context? Respond with only "yes" or "no"."""

    try:
        response = ollama.generate(
            model=DEFAULT_OLLAMA_MODEL,
            prompt=prompt,
            options={
                "temperature": 0.0,  # Low temperature for consistent responses
                "stop": ["\n"]
            }
        )
        answer = response['response'].strip().lower()

        # If the LLM says yes, the answer is grounded
        is_grounded = "yes" in answer
    except Exception as e:
        # If LLM fails, assume the answer is not grounded
        logger.exception("Error checking hallucination", e)
        is_grounded = False

    return {"is_grounded": is_grounded}

def broaden_query(state: RAGState) -> Dict[str, Any]:
    """Broaden the query to retrieve more documents"""
    logger.info(f"Broadening query: {state.rewritten_query} for question: {state.question}")
    prompt = f"""Broaden the following search query to retrieve more documents.
    Make it more general while still being relevant to the original question.

    Original question: {state.question}
    Current query: {state.rewritten_query}

    Broadened query:"""

    try:
        response = ollama.generate(
            model=DEFAULT_OLLAMA_MODEL,
            prompt=prompt,
            options={
                "temperature": 0.8,
                "top_p": 0.9,
                "stop": ["\n\n"]
            }
        )
        broadened_query = response['response'].strip()
        # If the LLM didn't generate a useful query, broaden by removing specific terms
        if not broadened_query or len(broadened_query) < 3:
            logger.warning("LLM didn't generate a useful broadened query, using simple broadening")
            # Simple broadening by removing some specific terms
            broadened_query = state.rewritten_query
    except Exception as e:
        # If LLM fails, use a simple broadening approach
        logger.exception("Error broadening query", e)
        broadened_query = state.rewritten_query

    return {"rewritten_query": broadened_query}

def increment_query_count(state: RAGState) -> Dict[str, Any]:
    """Increment the query retry count"""
    logger.info(f"Incrementing query retry count: {state.query_retry_count}")
    return {"query_retry_count": state.query_retry_count + 1}

def increment_answer_count(state: RAGState) -> Dict[str, Any]:
    """Increment the answer retry count"""
    logger.info(f"Incrementing answer retry count: {state.answer_retry_count}")
    return {"answer_retry_count": state.answer_retry_count + 1}

# Conditional edges
def enough_documents(state: RAGState) -> str:
    """Check if we have enough relevant documents"""
    logger.info(f"Checking if we have enough documents. Graded: {len(state.graded_documents)}, Retrieved: {len(state.documents)}")
    # If we have at least 2 relevant documents, proceed to generation
    # If we have no documents at all, go directly to generation (will produce "I don't have enough information")
    # Otherwise, try to broaden the query to get more documents
    if len(state.graded_documents) >= 2:
        return "generate"
    elif len(state.documents) == 0:
        # No documents were retrieved at all, no point in broadening
        return "generate"
    else:
        logger.info("No graded documents, considering answer as grounded")
        return "broaden"


def is_grounded(state: RAGState) -> str:
    """Check if the answer is grounded"""
    logger.info(f"Checking if answer is grounded. Graded documents: {len(state.graded_documents)}, Is grounded: {state.is_grounded}")
    # If we have no graded documents, the answer "I don't have enough information"
    # is considered grounded since it's the correct response when no information is available
    if len(state.graded_documents) == 0:
        logger.info("No graded documents, considering answer as grounded")
        return "return"
    return "return" if state.is_grounded else "regenerate"

def should_retry(state: RAGState) -> str:
    """Check if we should retry generation"""
    logger.info(f"Checking if we should retry generation. Retry count: {state.answer_retry_count}")
    return "generate" if state.answer_retry_count < 1 else "return"

def should_loop(state: RAGState) -> str:
    """Check if we should loop for more documents"""
    logger.info(f"Checking if we should loop for more documents. Retry count: {state.query_retry_count}")
    return "retrieve" if state.query_retry_count < 2 else "generate"

# Build the graph
def create_rag_graph():
    """Create the RAG graph"""
    logger.info("Creating RAG graph")
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("grade", grade_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("hallucination_check", check_hallucination)
    workflow.add_node("broaden", broaden_query)
    workflow.add_node("increment_query_count", increment_query_count)
    workflow.add_node("increment_answer_count", increment_answer_count)
    workflow.add_node("should_loop", should_loop)
    workflow.add_node("should_retry", should_retry)

    # Add edges
    workflow.set_entry_point("rewrite_query")
    workflow.add_edge("rewrite_query", "retrieve")
    workflow.add_edge("retrieve", "grade")
    workflow.add_conditional_edges(
        "grade",
        enough_documents,
        {
            "generate": "generate",
            "broaden": "increment_query_count"
        }
    )
    workflow.add_conditional_edges(
        "increment_query_count",
        should_loop,
        {
            "generate": "generate",
            "retrieve": "broaden"
        }
    )
    workflow.add_edge("broaden", "retrieve")

    workflow.add_edge("generate", "hallucination_check")
    workflow.add_conditional_edges(
        "hallucination_check",
        is_grounded,
        {
            "return": END,
            "regenerate": "increment_answer_count"
        }
    )
    workflow.add_conditional_edges(
        "increment_answer_count",
        should_retry,
        {
            "generate": "generate",
            "return": END
        }
    )

    return workflow.compile()

# Create the graph
rag_graph = create_rag_graph()