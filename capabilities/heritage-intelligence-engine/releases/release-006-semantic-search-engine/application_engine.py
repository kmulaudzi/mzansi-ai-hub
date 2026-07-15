"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 006 - Semantic Search Engine

Application Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from retrieval_engine import RetrievalEngine
from settings import MAX_RESULTS
from similarity_engine import SimilarityEngine


class ApplicationEngine:
    """
    Coordinates the interface and retrieval layers.

    The Application Engine validates user requests and coordinates
    the Retrieval Engine.

    It does not:

    - Load documents
    - Create chunks
    - Generate embeddings
    - Calculate similarity
    - Rank semantic results

    Those responsibilities belong to the specialised engines.
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        similarity_engine: SimilarityEngine,
        max_results: int = MAX_RESULTS,
    ):
        """
        Connect the engines required by the application.

        Dependencies are created in app.py and injected here.

        Parameters
        ----------
        providers
            Document providers such as MarkdownProvider
            and PDFProvider.

        chunking_engine
            Divides documents into smaller searchable chunks.

        embedding_engine
            Converts document chunks and user queries into vectors.

        similarity_engine
            Compares query vectors with cached chunk vectors.

        max_results
            Maximum number of results returned to the interface.
        """

        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero."
            )

        self.max_results = max_results

        # ---------------------------------------------------------
        # Retrieval Layer
        # ---------------------------------------------------------
        # The Application Engine injects all required dependencies
        # into the Retrieval Engine.
        #
        # The Retrieval Engine then coordinates:
        #
        # Providers
        #     ↓
        # Chunking Engine
        #     ↓
        # Embedding Engine
        #     ↓
        # Similarity Engine
        # ---------------------------------------------------------

        self.retrieval_engine = RetrievalEngine(
            providers=providers,
            chunking_engine=chunking_engine,
            embedding_engine=embedding_engine,
            similarity_engine=similarity_engine,
        )

    def prepare(self) -> int:
        """
        Prepare and cache the heritage knowledge once.

        Startup flow
        ------------
        Documents are loaded, chunked, embedded and stored
        in memory for repeated semantic searches.

        Returns
        -------
        int
            Number of embedded chunks cached in memory.
        """

        return self.retrieval_engine.prepare()

    def search(self, query: str) -> Dict:
        """
        Validate a user query and return semantic search results.

        Search-time flow
        ----------------
        User query
            ↓
        Retrieval Engine
            ↓
        Query embedding
            ↓
        Similarity comparison
            ↓
        Ranked semantic matches
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

        limited_results = results[
            : self.max_results
        ]

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
                f"Found {total_matches} semantic heritage match(es)."
            ),
        }