import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document
from typing import List, Dict, Any
import os

DEFAULT_PERSIST_DIRECTORY = "./chroma_db"

class VectorStore:
    """ChromaDB vector store wrapper"""

    def __init__(self, persist_directory: str = DEFAULT_PERSIST_DIRECTORY):
        """Initialize the vector store"""
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection("documents")

    def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """Add documents to the vector store"""
        ids = []
        contents = []
        metadatas = []

        for i, doc in enumerate(documents):
            ids.append(f"{doc.metadata.get('source', 'unknown')}_{i}")
            contents.append(doc.page_content)
            metadatas.append(doc.metadata)

        self.collection.add(
            ids=ids,
            documents=contents,
            metadatas=metadatas
        )

        print(f"Added {len(documents)} documents to the vector store")
        print(f"Total documents in the vector store: {self.collection.count()}")

        return {
            "added_count": len(documents),
            "total_count": self.collection.count()
        }

    def search(self, query: str, n_results: int = 5) -> List[Document]:
        """Search for similar documents"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        documents = []
        for i in range(len(results['ids'][0])):
            doc = Document(
                page_content=results['documents'][0][i],
                metadata=results['metadatas'][0][i]
            )
            documents.append(doc)

        return documents

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        count = self.collection.count()

        print(f"Vector store has {count} documents")

        # Get all documents to count unique sources
        if count > 0:
            all_docs = self.collection.get()
            sources = set()
            for metadata in all_docs['metadatas']:
                if 'source' in metadata:
                    sources.add(metadata['source'])
            file_count = len(sources)
        else:
            file_count = 0

        return {
            "file_count": file_count,
            "chunk_count": count
        }

    def reset(self) -> bool:
        """Reset the vector store"""
        # Delete the existing collection
        collection_name = self.collection.name
        self.client.delete_collection(name=collection_name)

        # Create a new collection with the same name
        self.collection = self.client.create_collection(name=collection_name)

        return True

# Global vector store instance
vectorStore = VectorStore()