"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 005 - Embedding Engine

Application Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from retrieval_engine import RetrievalEngine
from settings import MAX_RESULTS


class ApplicationEngine:
    """
    Coordinates the interface and retrieval layers.

    It does not load files, chunk documents, or create embeddings
    itself. Those responsibilities belong to the Retrieval Engine
    and its supporting engines.
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        max_results: int = MAX_RESULTS,
    ):
        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero."
            )

        self.max_results = max_results

        self.retrieval_engine = RetrievalEngine(
            providers=providers,
            chunking_engine=chunking_engine,
            embedding_engine=embedding_engine,
        )

    def prepare(self) -> int:
        """
        Prepare and cache the heritage knowledge once.
        """

        return self.retrieval_engine.prepare()

    def search(self, query: str) -> Dict:
        """
        Validate a query and return cached search results.
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

        results = self.retrieval_engine.retrieve(
            query=clean_query
        )

        total_matches = len(results)
        limited_results = results[: self.max_results]

        if not limited_results:
            return {
                "query": clean_query,
                "result_count": 0,
                "total_matches": 0,
                "results": [],
                "message": (
                    "No matching heritage knowledge was found."
                ),
            }

        return {
            "query": clean_query,
            "result_count": len(limited_results),
            "total_matches": total_matches,
            "results": limited_results,
            "message": (
                f"Found {total_matches} matching heritage chunk(s)."
            ),
        }