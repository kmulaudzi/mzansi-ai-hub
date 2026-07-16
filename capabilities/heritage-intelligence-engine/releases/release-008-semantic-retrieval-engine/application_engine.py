"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 007 - Vector Database Engine

Application Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from retrieval_engine import RetrievalEngine
from settings import MAX_RESULTS
from vector_database_engine import VectorDatabaseEngine


class ApplicationEngine:
    """
    Coordinates the user-facing application and retrieval layers.

    The Application Engine does not:

    - load documents
    - create chunks
    - generate embeddings
    - build the vector index
    - search FAISS directly

    Those responsibilities belong to the specialised engines.

    Its responsibilities are:

    - validate the user's query
    - request results from the Retrieval Engine
    - limit the number of returned results
    - return a stable response dictionary to the interface
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        vector_database_engine: VectorDatabaseEngine,
        max_results: int = MAX_RESULTS,
    ):
        """
        Connect the components required by the application.

        These dependencies are created in app.py and injected here.

        Parameters
        ----------
        providers
            Document providers such as MarkdownProvider
            and PDFProvider.

        chunking_engine
            Divides documents into smaller searchable chunks.

        embedding_engine
            Converts document chunks and user queries into vectors.

        vector_database_engine
            Builds and searches the FAISS vector index.

        max_results
            Maximum number of nearest-neighbour results returned
            to the interface.
        """

        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero."
            )

        self.max_results = max_results

        # ---------------------------------------------------------
        # Retrieval Layer
        # ---------------------------------------------------------
        # The Retrieval Engine coordinates the complete knowledge
        # preparation and retrieval workflow.
        #
        # Startup:
        #
        # Providers
        #     ↓
        # Chunking Engine
        #     ↓
        # Embedding Engine
        #     ↓
        # Vector Database Engine
        #
        # Search time:
        #
        # User query
        #     ↓
        # Embedding Engine
        #     ↓
        # Query embedding
        #     ↓
        # Vector Database Engine
        #     ↓
        # Nearest neighbours
        # ---------------------------------------------------------

        self.retrieval_engine = RetrievalEngine(
            providers=providers,
            chunking_engine=chunking_engine,
            embedding_engine=embedding_engine,
            vector_database_engine=vector_database_engine,
        )

    def prepare(self) -> int:
        """
        Prepare and index the heritage knowledge once.

        Startup flow
        ------------
        1. Load documents from all Providers.
        2. Divide the documents into chunks.
        3. Generate embeddings for every chunk.
        4. Build the FAISS vector index.
        5. Store the embedded chunk metadata in memory.

        Returns
        -------
        int
            Number of embedded chunks added to the vector index.
        """

        return self.retrieval_engine.prepare()

    def search(
        self,
        query: str,
    ) -> Dict:
        """
        Validate a query and return nearest-neighbour results.

        Search-time flow
        ----------------
        1. Validate the query.
        2. Send it to the Retrieval Engine.
        3. Convert the query into an embedding.
        4. Search the vector index.
        5. Return the nearest heritage chunks.

        Parameters
        ----------
        query
            User's natural-language heritage search query.

        Returns
        -------
        Dict
            Stable application response containing the query,
            result counts, message and nearest-neighbour results.
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
                    "No matching heritage knowledge was found."
                ),
            }

        return {
            "query": clean_query,
            "result_count": len(results),
            "total_matches": len(results),
            "results": results,
            "message": (
                f"Found {len(results)} nearest heritage match(es)."
            ),
        }