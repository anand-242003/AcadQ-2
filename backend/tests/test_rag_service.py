import pytest
from unittest.mock import MagicMock, patch


class TestRAGService:
    def _make_mock_doc(self, topic="study_habits", title="Test Resource",
                       url="https://example.com", description="A test resource"):
        doc = MagicMock()
        doc.metadata = {"topic": topic, "title": title, "url": url, "description": description}
        return doc

    def test_retrieve_resources_returns_list(self):
        """Test that retrieve_resources returns a list."""
        mock_store = MagicMock()
        mock_store.similarity_search.return_value = [self._make_mock_doc()]

        with patch.dict("sys.modules", {
            "langchain_community.vectorstores": MagicMock(),
            "langchain_community.embeddings": MagicMock(),
            "langchain.schema": MagicMock(),
        }):
            import importlib
            import sys
            # Remove cached module if present
            sys.modules.pop("services.rag_service", None)
            import services.rag_service as rag_module
            rag_module._vector_store = mock_store

            from services.rag_service import retrieve_resources
            results = retrieve_resources("study habits", k=3)
            assert isinstance(results, list)

    def test_retrieve_resources_returns_at_most_k(self):
        """Test that retrieve_resources returns at most k items."""
        mock_docs = [self._make_mock_doc(topic=f"t{i}", title=f"T{i}",
                                          url=f"https://example.com/{i}", description=f"D{i}")
                     for i in range(3)]
        mock_store = MagicMock()
        mock_store.similarity_search.return_value = mock_docs

        with patch.dict("sys.modules", {
            "langchain_community.vectorstores": MagicMock(),
            "langchain_community.embeddings": MagicMock(),
            "langchain.schema": MagicMock(),
        }):
            import sys
            sys.modules.pop("services.rag_service", None)
            import services.rag_service as rag_module
            rag_module._vector_store = mock_store

            from services.rag_service import retrieve_resources
            results = retrieve_resources("test query", k=3)
            assert len(results) <= 3

    def test_retrieve_resources_has_required_keys(self):
        """Test that each resource has required keys."""
        mock_store = MagicMock()
        mock_store.similarity_search.return_value = [
            self._make_mock_doc(topic="focus", title="Focus Guide",
                                url="https://example.com/focus", description="How to focus better")
        ]

        with patch.dict("sys.modules", {
            "langchain_community.vectorstores": MagicMock(),
            "langchain_community.embeddings": MagicMock(),
            "langchain.schema": MagicMock(),
        }):
            import sys
            sys.modules.pop("services.rag_service", None)
            import services.rag_service as rag_module
            rag_module._vector_store = mock_store

            from services.rag_service import retrieve_resources
            results = retrieve_resources("focus", k=1)
            if results:
                assert all(k in results[0] for k in ["topic", "title", "url", "description"])
