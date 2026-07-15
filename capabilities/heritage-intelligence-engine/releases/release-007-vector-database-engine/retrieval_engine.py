"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 007 - Vector Database Engine

Retrieval Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from vector_database_engine import VectorDatabaseEngine


class RetrievalEngine:
    """
    Coordinates knowledge preparation and vector retrieval.

    Startup flow
    ------------
    Providers
        ↓
    Documents
        ↓
    Chunking Engine
        ↓
    Chunks
        ↓
    Embedding Engine
        ↓
    Embedded Chunks
        ↓
    Vector Database Engine
        ↓
    Searchable Vector Index

    Search-time flow
    ----------------
    User Query
        ↓
    Embedding Engine
        ↓
    Query Embedding
        ↓
    Vector Database Engine
        ↓
    Nearest Heritage Chunks
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        vector_database_engine: VectorDatabaseEngine,
    ):
        """
        Connect all dependencies required for vector retrieval.

        The Retrieval Engine does not create its dependencies.
        They are created in app.py and injected here.
        """

        if not providers:
            raise ValueError(
                "RetrievalEngine requires at least one provider."
            )

        self.providers = providers
        self.chunking_engine = chunking_engine
        self.embedding_engine = embedding_engine
        self.vector_database_engine = vector_database_engine

        self.is_prepared = False

    def prepare(self) -> int:
        """
        Prepare and index the heritage knowledge once.

        Returns
        -------
        int
            Number of embedded chunks added to the vector index.
        """

        documents = []

        # ---------------------------------------------------------
        # Load documents
        # ---------------------------------------------------------

        for provider in self.providers:
            provider_documents = provider.load_documents()
            documents.extend(provider_documents)

        # ---------------------------------------------------------
        # Create chunks
        # ---------------------------------------------------------

        chunks = self.chunking_engine.chunk_documents(
            documents=documents
        )

        # ---------------------------------------------------------
        # Generate embeddings
        # ---------------------------------------------------------

        embedded_chunks = self.embedding_engine.embed_chunks(
            chunks=chunks
        )

        # ---------------------------------------------------------
        # Build vector index
        # ---------------------------------------------------------
        #
        # The Retrieval Engine delegates storage and indexing to the
        # Vector Database Engine.
        # ---------------------------------------------------------

        self.vector_database_engine.build_index(
            embedded_chunks=embedded_chunks
        )

        self.is_prepared = True

        return len(embedded_chunks)

    def retrieve(
        self,
        query: str,
        top_k: int,
    ) -> List[Dict]:
        """
        Retrieve the nearest heritage chunks from the vector index.

        Parameters
        ----------
        query : str
            User's natural-language search query.

        top_k : int
            Maximum number of nearest neighbours to return.

        Returns
        -------
        List[Dict]
            Nearest heritage chunks returned by the vector database.
        """

        if not self.is_prepared:
            raise RuntimeError(
                "RetrievalEngine is not prepared. "
                "Call prepare() before searching."
            )

        # Convert the user's query into the same vector space used
        # by the indexed heritage chunks.
        query_embedding = self.embedding_engine.embed_text(
            text=query
        )

        # Ask the Vector Database Engine for the nearest neighbours.
        return self.vector_database_engine.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )