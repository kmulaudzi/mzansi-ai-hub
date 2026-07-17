"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine

Application Engine
"""

from typing import Dict, List

from chunking_engine import ChunkingEngine
from context_engine import ContextEngine
from embedding_engine import EmbeddingEngine
from providers.base_provider import BaseProvider
from response_generation_engine import ResponseGenerationEngine
from retrieval_engine import RetrievalEngine
from retrieval_policy_engine import RetrievalPolicyEngine
from settings import MAX_RESULTS
from vector_database_engine import VectorDatabaseEngine


class ApplicationEngine:
    """
    Coordinates the complete user-facing AI workflow.

    Runtime flow
    ------------
    User Query
        ↓
    Retrieval Engine
        ↓
    Approved Chunks
        ↓
    Context Engine
        ↓
    LLM-Ready Context
        ↓
    Response Generation Engine
        ↓
    Grounded Heritage Answer

    The Application Engine coordinates these components.

    It does not perform embedding, vector search,
    policy evaluation, context formatting or text generation
    itself.
    """

    def __init__(
        self,
        providers: List[BaseProvider],
        chunking_engine: ChunkingEngine,
        embedding_engine: EmbeddingEngine,
        vector_database_engine: VectorDatabaseEngine,
        retrieval_policy_engine: RetrievalPolicyEngine,
        context_engine: ContextEngine,
        response_generation_engine: ResponseGenerationEngine,
        max_results: int = MAX_RESULTS,
    ):
        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero."
            )

        self.max_results = max_results

        # ---------------------------------------------------------
        # Retrieval capability
        # ---------------------------------------------------------
        #
        # The Retrieval Engine prepares the heritage knowledge and
        # retrieves approved chunks for each user query.
        # ---------------------------------------------------------

        self.retrieval_engine = RetrievalEngine(
            providers=providers,
            chunking_engine=chunking_engine,
            embedding_engine=embedding_engine,
            vector_database_engine=vector_database_engine,
            retrieval_policy_engine=retrieval_policy_engine,
        )

        # ---------------------------------------------------------
        # Context capability
        # ---------------------------------------------------------
        #
        # Converts approved chunks into one structured context
        # string suitable for the language model.
        # ---------------------------------------------------------

        self.context_engine = context_engine

        # ---------------------------------------------------------
        # Response-generation capability
        # ---------------------------------------------------------
        #
        # Generates the final grounded answer using the user query
        # and the context prepared from heritage documents.
        # ---------------------------------------------------------

        self.response_generation_engine = (
            response_generation_engine
        )

    def prepare(self) -> int:
        """
        Prepare and index the heritage knowledge once.

        This is called during application startup.
        """

        return self.retrieval_engine.prepare()

    def ask(
        self,
        query: str,
    ) -> Dict:
        """
        Answer a heritage question using retrieved knowledge.

        Parameters
        ----------
        query : str
            User's natural-language question.

        Returns
        -------
        Dict
            Stable application response containing the query,
            answer, context and approved sources.
        """

        clean_query = query.strip()

        if not clean_query:
            return {
                "query": "",
                "answer": "",
                "context": "",
                "result_count": 0,
                "results": [],
                "message": "Please enter a heritage question.",
            }

        # ---------------------------------------------------------
        # Step 1: Retrieve approved heritage chunks
        # ---------------------------------------------------------

        approved_chunks = self.retrieval_engine.retrieve(
            query=clean_query,
            top_k=self.max_results,
        )

        if not approved_chunks:
            fallback_message = (
                "The available heritage documents do not "
                "contain enough information."
            )

            return {
                "query": clean_query,
                "answer": fallback_message,
                "context": "",
                "result_count": 0,
                "results": [],
                "message": (
                    "No heritage knowledge passed the "
                    "retrieval policies."
                ),
            }

        # ---------------------------------------------------------
        # Step 2: Build LLM-ready context
        # ---------------------------------------------------------

        context = self.context_engine.build_context(
            approved_chunks=approved_chunks
        )

        if not context:
            fallback_message = (
                "The available heritage documents do not "
                "contain enough information."
            )

            return {
                "query": clean_query,
                "answer": fallback_message,
                "context": "",
                "result_count": len(approved_chunks),
                "results": approved_chunks,
                "message": (
                    "Approved chunks contained no usable "
                    "context."
                ),
            }

        # ---------------------------------------------------------
        # Step 3: Generate the grounded answer
        # ---------------------------------------------------------

        answer = (
            self.response_generation_engine.generate_response(
                query=clean_query,
                context=context,
            )
        )

        return {
            "query": clean_query,
            "answer": answer,
            "context": context,
            "result_count": len(approved_chunks),
            "results": approved_chunks,
            "message": (
                f"Answer generated from "
                f"{len(approved_chunks)} approved "
                "heritage chunk(s)."
            ),
        }