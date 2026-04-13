import os
import json
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_PATH = BASE_DIR / "data" / "resources.json"
CHROMA_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "acadiq_resources"

_embeddings: HuggingFaceEmbeddings | None = None
_vector_store: Chroma | None = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def initialize_vector_store() -> None:
    """
    Idempotent initialization of ChromaDB vector store from resources.json.
    Skips re-embedding if collection already has documents.
    """
    global _vector_store

    embeddings = _get_embeddings()

    # Try to load existing store first
    try:
        existing = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
        )
        if existing._collection.count() > 0:
            _vector_store = existing
            print(f"[RAG] Loaded existing ChromaDB collection ({existing._collection.count()} docs)")
            return
    except Exception:
        pass

    # Build from resources.json
    if not RESOURCES_PATH.exists():
        print(f"[RAG] Warning: resources.json not found at {RESOURCES_PATH}")
        return

    with open(RESOURCES_PATH, "r") as f:
        resources = json.load(f)

    documents = []
    for resource in resources:
        doc = Document(
            page_content=f"{resource['topic']}: {resource['description']}",
            metadata={
                "topic": resource["topic"],
                "title": resource["title"],
                "url": resource["url"],
                "description": resource["description"],
            },
        )
        documents.append(doc)

    _vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )
    print(f"[RAG] Initialized ChromaDB with {len(documents)} resources")


def retrieve_resources(query: str, k: int = 3) -> list[dict]:
    """
    Retrieve k most relevant resources by cosine similarity.
    Returns list of dicts with topic, title, url, description.
    """
    global _vector_store

    if _vector_store is None:
        initialize_vector_store()

    if _vector_store is None:
        return []

    try:
        results = _vector_store.similarity_search(query, k=k)
        return [
            {
                "topic": doc.metadata.get("topic", ""),
                "title": doc.metadata.get("title", ""),
                "url": doc.metadata.get("url", ""),
                "description": doc.metadata.get("description", ""),
            }
            for doc in results
        ]
    except Exception as e:
        print(f"[RAG] Retrieval error: {e}")
        return []
