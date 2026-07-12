from typing import Dict, List

from providers.base_provider import BaseProvider
from search_engine import search_documents


class RetrievalEngine:
    """
    Coordinates retrieval across one or more document providers.
    """

    def __init__(
        self,
        providers: List[BaseProvider],
    ):
        if not providers:
            raise ValueError(
                "RetrievalEngine requires at least one provider."
            )

        self.providers = providers

    def retrieve(self, query: str) -> List[Dict]:
        """
        Load documents from all providers and return ranked matches.
        """

        documents = []

        for provider in self.providers:
            provider_documents = provider.load_documents()
            documents.extend(provider_documents)

        return search_documents(
            query=query,
            documents=documents,
        )