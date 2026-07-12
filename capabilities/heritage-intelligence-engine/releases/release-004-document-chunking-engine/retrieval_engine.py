from typing import Dict, List

from chunking_engine import ChunkingEngine
from providers.base_provider import BaseProvider
from search_engine import search_documents


class RetrievalEngine:
    """
    Coordinates retrieval across document providers.

    Flow:
    Providers
        ↓
    Documents
        ↓
    Chunking Engine
        ↓
    Search Engine
        ↓
    Ranked Chunks
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
    ):
        if not providers:
            raise ValueError(
                "RetrievalEngine requires at least one provider."
            )

        self.providers = providers
        self.chunking_engine = chunking_engine

    def retrieve(self, query: str) -> List[Dict]:
        """
        Load documents, create chunks and return ranked matches.
        """

        documents = []

        for provider in self.providers:
            provider_documents = provider.load_documents()
            documents.extend(provider_documents)

        chunks = self.chunking_engine.chunk_documents(
            documents=documents
        )

        return search_documents(
            query=query,
            documents=chunks,
        )