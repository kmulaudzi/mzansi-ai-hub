from typing import Dict, List

from knowledge_loader import load_knowledge_cards
from search_engine import search_knowledge


class RetrievalEngine:
    """
    Coordinates the heritage knowledge retrieval process.

    Responsibilities
    ----------------
    - Load heritage knowledge.
    - Pass user queries to the Search Engine.
    - Return ranked search results.

    Future releases may extend this engine to retrieve content
    from PDFs, vector databases, audio, images and other sources.
    """

    def __init__(self, dataset_path: str):
        """
        Initialize the Retrieval Engine.

        Parameters
        ----------
        dataset_path : str
            Path containing the heritage Knowledge Cards.
        """

        self.dataset_path = dataset_path

        self.knowledge_cards = load_knowledge_cards(
            dataset_path=self.dataset_path
        )

    def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve ranked Knowledge Cards for a user query.

        Parameters
        ----------
        query : str
            User search query.

        Returns
        -------
        List[Dict]
            Ranked matching Knowledge Cards.
        """

        return search_knowledge(
            query=query,
            knowledge_cards=self.knowledge_cards,
        )