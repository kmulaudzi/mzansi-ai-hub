from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from search_engine import search_documents


class RetrievalEngine:
    """
    Coordinates document loading, chunking, embedding,
    and keyword retrieval.
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

    def prepare_documents(self) -> List[Dict]:
        """
        Load documents, split them into chunks,
        and generate embeddings.
        """

        documents = []

        for provider in self.providers:
            documents.extend(
                provider.load_documents()
            )

        chunks = self.chunking_engine.chunk_documents(
            documents=documents
        )

        return self.embedding_engine.embed_chunks(
            chunks=chunks
        )

    def retrieve(self, query: str) -> List[Dict]:
        """
        Continue using keyword search for this release.

        Semantic retrieval will be introduced in a later release.
        """

        embedded_chunks = self.prepare_documents()

        return search_documents(
            query=query,
            documents=embedded_chunks,
        )