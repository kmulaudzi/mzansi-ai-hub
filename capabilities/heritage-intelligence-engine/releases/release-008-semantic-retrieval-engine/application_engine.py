"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 008 - Retrieval Policy Engine

Application Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from retrieval_engine import RetrievalEngine
from retrieval_policy_engine import RetrievalPolicyEngine
from settings import MAX_RESULTS
from vector_database_engine import VectorDatabaseEngine


class ApplicationEngine:
    """
    Coordinates the user-facing application.

    Responsibilities
    ----------------
    - Validate user input
    - Coordinate retrieval
    - Return a stable response structure

    It does not perform retrieval,
    embedding or policy evaluation itself.
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        vector_database_engine: VectorDatabaseEngine,
        retrieval_policy_engine: RetrievalPolicyEngine,
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
            vector_database_engine=vector_database_engine,
            retrieval_policy_engine=retrieval_policy_engine,
        )

    def prepare(self) -> int:
        """
        Prepare the heritage knowledge once.
        """

        return self.retrieval_engine.prepare()

    def search(
        self,
        query: str,
    ) -> Dict:
        """
        Validate a query and return approved
        retrieval results.
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
            query=clean_query,
            top_k=self.max_results,
        )

        if not results:
            return {
                "query": clean_query,
                "result_count": 0,
                "total_matches": 0,
                "results": [],
                "message": (
                    "No heritage knowledge passed "
                    "the retrieval policies."
                ),
            }

        return {
            "query": clean_query,
            "result_count": len(results),
            "total_matches": len(results),
            "results": results,
            "message": (
                f"{len(results)} heritage chunk(s) "
                "approved by the retrieval policies."
            ),
        }