"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 008 - Retrieval Policy Engine

Retrieval Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from retrieval_policy_engine import RetrievalPolicyEngine
from vector_database_engine import VectorDatabaseEngine


class RetrievalEngine:
    """
    Coordinates knowledge preparation and policy-controlled retrieval.

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
    Candidate Chunks
        ↓
    Retrieval Policy Engine
        ↓
    Approved Chunks
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        vector_database_engine: VectorDatabaseEngine,
        retrieval_policy_engine: RetrievalPolicyEngine,
    ):
        """
        Connect all dependencies required for retrieval.

        The Retrieval Engine does not create these components.
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
        self.retrieval_policy_engine = retrieval_policy_engine

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
        # Build the vector index
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
        Retrieve and approve heritage knowledge.

        Parameters
        ----------
        query : str
            User's natural-language query.

        top_k : int
            Number of nearest-neighbour candidates requested
            from the Vector Database Engine.

        Returns
        -------
        List[Dict]
            Candidate chunks that passed the retrieval policies.
        """

        if not self.is_prepared:
            raise RuntimeError(
                "RetrievalEngine is not prepared. "
                "Call prepare() before searching."
            )

        # ---------------------------------------------------------
        # Create the query embedding
        # ---------------------------------------------------------

        query_embedding = self.embedding_engine.embed_text(
            text=query
        )

        # ---------------------------------------------------------
        # Retrieve candidates from semantic memory
        # ---------------------------------------------------------
        #
        # These are only candidates.
        # The Vector Database finds close vectors, but it does not
        # decide whether they are relevant enough to continue.
        # ---------------------------------------------------------

        candidate_chunks = self.vector_database_engine.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        # ---------------------------------------------------------
        # Apply retrieval policies
        # ---------------------------------------------------------
        #
        # The Retrieval Policy Engine evaluates the candidates.
        #
        # Release 008 policy:
        # similarity >= configured threshold
        # ---------------------------------------------------------

        approved_chunks = self.retrieval_policy_engine.apply(
            candidate_chunks=candidate_chunks
        )

        return approved_chunks