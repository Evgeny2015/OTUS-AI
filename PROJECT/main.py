import os
import asyncio
from fastmcp import FastMCP
import glob
from document_loader import load_document
import ollama
from rag_pipeline import rag_graph, RAGState, DEFAULT_OLLAMA_MODEL
from vector_store import vectorStore

# Initialize FastMCP
mcp = FastMCP("RAG Knowledge Base")

# Environment variables
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

@mcp.tool(
    name="index_folder",
    description="Indexes documents in a folder"
)
async def index_folder(folder_path: str, glob_pattern: str = "**/*"):
    """Index documents in a folder"""
    # Create the full pattern
    full_pattern = os.path.join(folder_path, glob_pattern)

    # Find all matching files
    file_paths = glob.glob(full_pattern, recursive=True)

    # Filter out directories
    file_paths = [f for f in file_paths if os.path.isfile(f)]

    total_documents = 0
    indexed_files = 0

    print(f"Found {len(file_paths)} files to index")

    # Process each file
    for file_path in file_paths:
        try:
            # Load the document
            documents = load_document(file_path)

            print(f"Indexing file {file_path} with {len(documents)} chunks")

            # Add to vector store
            result = vectorStore.add_documents(documents)
            total_documents += result["added_count"]
            indexed_files += 1

        except Exception as e:
            print(f"Error indexing file {file_path}: {e}")
            continue

    return {
        "status": "success",
        "message": f"Indexed {indexed_files} files with {total_documents} document chunks",
        "indexed_files": indexed_files,
        "total_documents": total_documents
    }

@mcp.tool(
    name="ask_question",
    description="Ask a question based on indexed documents"
)
async def ask_question(question: str):
    """Ask a question based on indexed documents"""
    # Create initial state
    initial_state = RAGState(
        question=question,
        rewritten_query="",
        documents=[],
        graded_documents=[],
        generation="",
        sources=[],
        query_retry_count=0,
        answer_retry_count=0,
        is_grounded=False
    )

    # Run the RAG graph
    final_state = rag_graph.invoke(initial_state)

    # Extract sources from graded documents
    sources = []
    for doc in final_state["graded_documents"]:
        if 'source' in doc.metadata:
            sources.append(doc.metadata['source'])

    # Remove duplicates from sources
    sources = list(set(sources))

    return {
        "answer": final_state["generation"],
        "sources": sources,
        "is_grounded": final_state["is_grounded"]
    }

@mcp.tool(
    name="find_relevant_docs",
    description="Find relevant documents for a query"
)
async def find_relevant_docs(query: str, top_k: int = 5):
    """Find relevant documents for a query"""
    # Search for relevant documents
    documents = vectorStore.search(query, n_results=top_k)

    # Convert documents to serializable format
    docs_list = []
    for doc in documents:
        docs_list.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })

    return {
        "documents": docs_list,
        "query": query,
        "count": len(docs_list)
    }

@mcp.tool(
    name="summarize_document",
    description="Summarize a document"
)
async def summarize_document(file_path: str):
    """Summarize a document"""
    # Load the document
    documents = load_document(file_path)

    # Combine all chunks into one text
    full_text = "\n\n".join([doc.page_content for doc in documents])

    # Use Ollama to generate a summary
    try:
        response = ollama.generate(
            model=DEFAULT_OLLAMA_MODEL,
            prompt=f"Please summarize the following document:\n\n{full_text[:4000]}",
            options={
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
        summary = response['response'].strip()
    except Exception as e:
        summary = f"Error generating summary: {e}"

    return {
        "summary": summary,
        "file_path": file_path,
        "chunk_count": len(documents)
    }

@mcp.tool(
    name="index_status",
    description="Get the status of the index"
)
async def index_status():
    """Get the status of the index"""
    # Get statistics from vector store
    stats = vectorStore.get_stats()
    return {
        "file_count": stats["file_count"],
        "chunk_count": stats["chunk_count"],
        "last_indexed": None  # This would require additional tracking
    }

if __name__ == "__main__":
    mcp.run()