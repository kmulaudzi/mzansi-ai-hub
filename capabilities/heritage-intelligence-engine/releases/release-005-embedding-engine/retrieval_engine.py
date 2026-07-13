"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 005 - Embedding Engine

Retrieval Engine with in-memory caching
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from search_engine import search_documents


class RetrievalEngine:
    """
    Coordinates document preparation and retrieval.

    Expensive preparation happens once:

    Providers
        ↓
    Documents
        ↓
    Chunking Engine
        ↓
    Embedding Engine
        ↓
    Cached Embedded Chunks

    Every user search then reuses the cached chunks.
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
    ):
        if not providers:
            raise ValueError(
                "RetrievalEngine requires at least one provider."
            )

        self.providers = providers
        self.chunking_engine = chunking_engine
        self.embedding_engine = embedding_engine

        # Empty until prepare() runs.
        self.cached_chunks: List[Dict] = []
        self.is_prepared = False

    def prepare(self) -> int:
        """
        Load, chunk and embed all documents once.

        Returns
        -------
        int
            Number of embedded chunks stored in memory.
        """

        documents = []

        for provider in self.providers:
            provider_documents = provider.load_documents()
            documents.extend(provider_documents)

        chunks = self.chunking_engine.chunk_documents(
            documents=documents
        )

        self.cached_chunks = self.embedding_engine.embed_chunks(
            chunks=chunks
        )

        self.is_prepared = True

        return len(self.cached_chunks)

    def retrieve(self, query: str) -> List[Dict]:
        """
        Search the already prepared and cached chunks.
        """

        if not self.is_prepared:
            raise RuntimeError(
                "RetrievalEngine is not prepared. "
                "Call prepare() before searching."
            )

        return search_documents(
            query=query,
            documents=self.cached_chunks,
        )