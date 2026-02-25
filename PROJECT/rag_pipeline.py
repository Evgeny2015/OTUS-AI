import os
import ollama
from vector_store import vectorStore
from typing import List, Dict, Any
from langchain_core.documents import Document
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
import asyncio

class RAGState(BaseModel):
    """State for the RAG pipeline"""
    question: str = Field(description="The original question")
    rewritten_query: str = Field(description="The rewritten query for search")
    documents: List[Document] = Field(description="Retrieved documents")
    graded_documents: List[Document] = Field(description="Graded documents")
    generation: str = Field(description="Generated answer")
    sources: List[str] = Field(description="Source documents")
    retry_count: int = Field(description="Number of retries")
    is_grounded: bool = Field(description="Whether the answer is grounded")

# Node functions
def rewrite_query(state: RAGState) -> Dict[str, Any]:
    """Rewrite the query to improve search results"""
    # Use an LLM to rewrite the query for better search results
    prompt = f"""Rewrite the following question to improve search results.
    Make it more specific and focused on finding relevant information.

    Original question: {state.question}

    Rewritten query:"""

    try:
        response = ollama.generate(
            model="llama3",
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["\n\n"]
            }
        )
        rewritten_query = response['response'].strip()
        # If the LLM didn't generate a useful query, fall back to the original
        if not rewritten_query or len(rewritten_query) < 3:
            rewritten_query = state.question
    except Exception:
        # If LLM fails, use the original query
        rewritten_query = state.question

    return {"rewritten_query": rewritten_query}

def retrieve_documents(state: RAGState) -> Dict[str, Any]:
    """Retrieve documents based on the query"""
    # Use the vector store to retrieve relevant documents
    try:
        documents = vectorStore.search(state.rewritten_query, n_results=10)
    except Exception:
        # If retrieval fails, return empty list
        documents = []

    return {"documents": documents}

def grade_documents(state: RAGState) -> Dict[str, Any]:
    """Grade documents for relevance"""
    if not state.documents:
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
                model="llama3",
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
        except Exception:
            # If LLM fails, include the document by default
            graded_documents.append(doc)

    return {"graded_documents": graded_documents}

def generate_answer(state: RAGState) -> Dict[str, Any]:
    """Generate an answer based on the documents"""
    if not state.graded_documents:
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
            model="llama3",
            prompt=prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        generation = response['response'].strip()
    except Exception:
        # If LLM fails, provide a fallback answer
        generation = "I'm sorry, but I'm having trouble generating an answer right now."

    return {"generation": generation}

def check_hallucination(state: RAGState) -> Dict[str, Any]:
    """Check if the answer is grounded in the documents"""
    if not state.graded_documents or not state.generation:
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
            model="llama3",
            prompt=prompt,
            options={
                "temperature": 0.0,  # Low temperature for consistent responses
                "stop": ["\n"]
            }
        )
        answer = response['response'].strip().lower()

        # If the LLM says yes, the answer is grounded
        is_grounded = "yes" in answer
    except Exception:
        # If LLM fails, assume the answer is not grounded
        is_grounded = False

    return {"is_grounded": is_grounded}

def broaden_query(state: RAGState) -> Dict[str, Any]:
    """Broaden the query to retrieve more documents"""
    # Use an LLM to broaden the query to retrieve more documents
    prompt = f"""Broaden the following search query to retrieve more documents.
    Make it more general while still being relevant to the original question.

    Original question: {state.question}
    Current query: {state.rewritten_query}

    Broadened query:"""

    try:
        response = ollama.generate(
            model="llama3",
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
            # Simple broadening by removing some specific terms
            broadened_query = state.rewritten_query
    except Exception:
        # If LLM fails, use a simple broadening approach
        broadened_query = state.rewritten_query

    return {"rewritten_query": broadened_query}

# Conditional edges
def enough_documents(state: RAGState) -> str:
    """Check if we have enough relevant documents"""
    # If we have at least 2 relevant documents, proceed to generation
    # Otherwise, try to broaden the query to get more documents
    return "generate" if len(state.graded_documents) >= 2 else "broaden"

def is_grounded(state: RAGState) -> str:
    """Check if the answer is grounded"""
    return "return" if state.is_grounded else "regenerate"

def should_retry(state: RAGState) -> str:
    """Check if we should retry generation"""
    return "generate" if state.retry_count < 1 else "return"

def increment_retry_count(state: RAGState) -> Dict[str, Any]:
    """Increment the retry count"""
    return {"retry_count": state.retry_count + 1}

def should_loop(state: RAGState) -> str:
    """Check if we should loop for more documents"""
    return "retrieve" if state.retry_count < 2 else "generate"

# Build the graph
def create_rag_graph():
    """Create the RAG graph"""
    workflow = StateGraph(RAGState)

    # Add nodes
    workflow.add_node("rewrite_query", rewrite_query)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("grade", grade_documents)
    workflow.add_node("generate", generate_answer)
    workflow.add_node("hallucination_check", check_hallucination)
    workflow.add_node("broaden", broaden_query)
    workflow.add_node("increment_retry", increment_retry_count)

    # Add edges
    workflow.set_entry_point("rewrite_query")
    workflow.add_edge("rewrite_query", "retrieve")
    workflow.add_edge("retrieve", "grade")
    workflow.add_conditional_edges(
        "grade",
        enough_documents,
        {
            "generate": "generate",
            "broaden": "broaden"
        }
    )
    workflow.add_edge("broaden", "retrieve")
    workflow.add_edge("generate", "hallucination_check")
    workflow.add_conditional_edges(
        "hallucination_check",
        is_grounded,
        {
            "return": END,
            "regenerate": "increment_retry"
        }
    )
    workflow.add_edge("increment_retry", "generate")

    return workflow.compile()

# Create the graph
rag_graph = create_rag_graph()