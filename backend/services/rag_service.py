import os
import json
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_RESOURCES_DIR = BASE_DIR / "data" / "resoureces"
RESOURCES_PATH = BASE_DIR / "data" / "resources.json"
CHROMA_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "acadiq_resources_pdfs_v1"

_embeddings: HuggingFaceEmbeddings | None = None
_vector_store: Chroma | None = None


def _chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    normalized = " ".join((text or "").split())
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    text_len = len(normalized)
    while start < text_len:
        end = min(text_len, start + chunk_size)
        chunks.append(normalized[start:end])
        if end >= text_len:
            break
        start = max(0, end - overlap)
    return chunks


def _infer_topic_from_filename(filename: str) -> str:
    lower = filename.lower()
    if "sleep" in lower:
        return "sleep"
    if "procrast" in lower:
        return "procrastination"
    if "motivation" in lower or "dweck" in lower:
        return "motivation"
    if "cognitive" in lower or "load" in lower or "sweller" in lower:
        return "cognitive_load"
    if "self-regulated" in lower or "zimmerman" in lower:
        return "self_regulated_learning"
    if "retrieval" in lower or "dunloski" in lower or "cepeda" in lower:
        return "study_strategies"
    return "research_paper"


def _load_pdf_documents() -> list[Document]:
    if not PDF_RESOURCES_DIR.exists():
        return []

    pdf_files = sorted(PDF_RESOURCES_DIR.glob("*.pdf"))
    if not pdf_files:
        return []

    documents: list[Document] = []
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(str(pdf_file))
        except Exception as exc:
            print(f"[RAG] Skipping unreadable PDF {pdf_file.name}: {exc}")
            continue

        topic = _infer_topic_from_filename(pdf_file.name)
        title = pdf_file.stem
        for page_idx, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            for chunk_idx, chunk in enumerate(_chunk_text(page_text), start=1):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "topic": topic,
                            "title": title,
                            "url": pdf_file.name,
                            "description": chunk[:280],
                            "source_file": pdf_file.name,
                            "page": page_idx,
                            "chunk": chunk_idx,
                        },
                    )
                )

    return documents


def _load_legacy_json_documents() -> list[Document]:
    if not RESOURCES_PATH.exists():
        return []

    with open(RESOURCES_PATH, "r", encoding="utf-8") as f:
        resources = json.load(f)

    documents: list[Document] = []
    for resource in resources:
        documents.append(
            Document(
                page_content=f"{resource['topic']}: {resource['description']}",
                metadata={
                    "topic": resource["topic"],
                    "title": resource["title"],
                    "url": resource["url"],
                    "description": resource["description"],
                },
            )
        )

    return documents


def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings


def initialize_vector_store() -> None:
    """
    Idempotent initialization of ChromaDB vector store.
    Priority source is backend/data/resoureces/*.pdf.
    Falls back to data/resources.json if no PDFs are available.
    """
    global _vector_store

    embeddings = _get_embeddings()


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

    documents = _load_pdf_documents()
    source_label = "PDF resources folder"
    if not documents:
        documents = _load_legacy_json_documents()
        source_label = "resources.json"

    if not documents:
        print(f"[RAG] Warning: no resources found in {PDF_RESOURCES_DIR} or {RESOURCES_PATH}")
        return

    _vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )
    print(f"[RAG] Initialized ChromaDB with {len(documents)} chunks from {source_label}")


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
        results = _vector_store.max_marginal_relevance_search(
            query,
            k=max(k * 6, k),
            fetch_k=max(k * 20, 40),
        )
        if not results:
            results = _vector_store.similarity_search(query, k=max(k * 12, k))

        items: list[dict[str, Any]] = []
        seen_titles: set[str] = set()

        for doc in results:
            title = doc.metadata.get("title", "")
            page = doc.metadata.get("page")
            title_key = title.lower().strip()
            if title_key in seen_titles:
                continue

            seen_titles.add(title_key)
            description = doc.metadata.get("description") or (doc.page_content or "")[:280]
            if page:
                description = f"{description} (page {page})"

            items.append(
                {
                    "topic": doc.metadata.get("topic", "research_paper"),
                    "title": title or doc.metadata.get("source_file", "Research Resource"),
                    "url": doc.metadata.get("url", ""),
                    "description": description,
                }
            )

            if len(items) >= k:
                break

        if len(items) < k:
            fallback_results = _vector_store.similarity_search(query, k=max(k * 20, k))
            for doc in fallback_results:
                title = doc.metadata.get("title", "")
                title_key = title.lower().strip()
                if title_key in seen_titles:
                    continue

                seen_titles.add(title_key)
                page = doc.metadata.get("page")
                description = doc.metadata.get("description") or (doc.page_content or "")[:280]
                if page:
                    description = f"{description} (page {page})"

                items.append(
                    {
                        "topic": doc.metadata.get("topic", "research_paper"),
                        "title": title or doc.metadata.get("source_file", "Research Resource"),
                        "url": doc.metadata.get("url", ""),
                        "description": description,
                    }
                )

                if len(items) >= k:
                    break

        if len(items) < k:
            try:
                collection_dump = _vector_store._collection.get(include=["metadatas"], limit=5000)
                for metadata in collection_dump.get("metadatas", []):
                    if not isinstance(metadata, dict):
                        continue

                    title = metadata.get("title", "")
                    title_key = title.lower().strip()
                    if not title_key or title_key in seen_titles:
                        continue

                    seen_titles.add(title_key)
                    page = metadata.get("page")
                    description = metadata.get("description", "")
                    if page and description:
                        description = f"{description} (page {page})"

                    items.append(
                        {
                            "topic": metadata.get("topic", "research_paper"),
                            "title": title,
                            "url": metadata.get("url", ""),
                            "description": description,
                        }
                    )

                    if len(items) >= k:
                        break
            except Exception:
                pass

        return items
    except Exception as e:
        print(f"[RAG] Retrieval error: {e}")
        return []
