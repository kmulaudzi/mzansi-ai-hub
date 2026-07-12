from typing import Dict, List

from retrieval_engine import RetrievalEngine
from settings import MAX_RESULTS


class ApplicationEngine:
    """
    Coordinates requests between the interface and retrieval layers.

    Responsibilities
    ----------------
    - Validate user input.
    - Call the Retrieval Engine.
    - Limit the number of results.
    - Return a consistent response structure.
    """

    def __init__(
        self,
        dataset_path: str,
        max_results: int = MAX_RESULTS,
    ):
        """
        Initialize the Application Engine.

        Parameters
        ----------
        dataset_path : str
            Path containing the heritage Knowledge Cards.

        max_results : int
            Maximum number of results returned to the interface.
        """

        if max_results <= 0:
            raise ValueError("max_results must be greater than zero.")

        self.max_results = max_results

        self.retrieval_engine = RetrievalEngine(
            dataset_path=dataset_path
        )

    def search(self, query: str) -> Dict:
        """
        Process a complete heritage search request.

        Parameters
        ----------
        query : str
            User search query.

        Returns
        -------
        Dict
            Application response containing:
            - query
            - result_count
            - total_matches
            - results
            - message
        """

        clean_query = query.strip()

        if not clean_query:
            return {
                "query": "",
                "result_count": 0,
                "total_matches": 0,
                "results": [],
                "message": "Please enter a search query.",
            }

        results: List[Dict] = self.retrieval_engine.retrieve(
            clean_query
        )

        total_matches = len(results)

        limited_results = results[: self.max_results]

        if not limited_results:
            return {
                "query": clean_query,
                "result_count": 0,
                "total_matches": 0,
                "results": [],
                "message": "No matching heritage knowledge was found.",
            }

        return {
            "query": clean_query,
            "result_count": len(limited_results),
            "total_matches": total_matches,
            "results": limited_results,
            "message": (
                f"Found {total_matches} matching heritage result(s)."
            ),
        }