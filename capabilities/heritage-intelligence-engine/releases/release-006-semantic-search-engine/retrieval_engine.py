"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 006 - Semantic Search Engine

Retrieval Engine with in-memory caching
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from similarity_engine import SimilarityEngine


class RetrievalEngine:
    """
    Coordinates document preparation and semantic retrieval.

    Startup flow
    ------------
    Providers
        ↓
    Documents
        ↓
    Chunking Engine
        ↓
    Embedding Engine
        ↓
    Cached Embedded Chunks

    Search-time flow
    ----------------
    User Query
        ↓
    Embedding Engine
        ↓
    Query Embedding
        ↓
    Similarity Engine
        ↓
    Ranked Semantic Matches
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        similarity_engine: SimilarityEngine,
    ):
        """
        Connect the engines required for semantic retrieval.

        The Retrieval Engine does not create these dependencies.
        They are injected from the application runtime.
        """

        if not providers:
            raise ValueError(
                "RetrievalEngine requires at least one provider."
            )

        self.providers = providers
        self.chunking_engine = chunking_engine
        self.embedding_engine = embedding_engine
        self.similarity_engine = similarity_engine

        # Empty until prepare() runs.
        self.cached_chunks: List[Dict] = []
        self.is_prepared = False

    def prepare(self) -> int:
        """
        Load, chunk and embed all heritage documents once.

        This is the expensive startup workflow.

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
        Search cached heritage chunks using semantic similarity.

        Parameters
        ----------
        query : str
            User's natural-language search query.

        Returns
        -------
        List[Dict]
            Cached chunks enriched with similarity scores,
            sorted from most semantically similar to least similar.
        """

        if not self.is_prepared:
            raise RuntimeError(
                "RetrievalEngine is not prepared. "
                "Call prepare() before searching."
            )

        # Convert the user's question into the same vector space
        # used for the cached heritage chunks.
        query_embedding = self.embedding_engine.embed_text(
            text=query
        )

        # Compare the query vector against every cached chunk vector.
        return self.similarity_engine.compare(
            query_embedding=query_embedding,
            embedded_chunks=self.cached_chunks,
        )