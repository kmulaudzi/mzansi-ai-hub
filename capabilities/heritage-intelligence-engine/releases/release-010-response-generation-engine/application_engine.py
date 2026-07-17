"""
Application Engine

Release 010B - Full Heritage Intelligence Engine Integration

The Application Engine coordinates the complete user-facing
heritage question-answering workflow.

Runtime flow:

User Question
    ↓
Retrieval Engine
    ↓
Approved Heritage Chunks
    ↓
Context Engine
    ↓
LLM-Ready Context
    ↓
Response Generation Engine
    ↓
Grounded Heritage Answer

The Application Engine does not perform retrieval, chunking,
embedding, context formatting, prompt construction, or model
generation itself.

It delegates each responsibility to the appropriate engine.
"""

from typing import Any, Dict, List

from retrieval_engine import RetrievalEngine


class ApplicationEngine:
    """
    Coordinates the complete Heritage Intelligence Engine workflow.
    """

    def __init__(
        self,
        providers,
        chunking_engine,
        embedding_engine,
        vector_database_engine,
        retrieval_policy_engine,
        context_engine,
        response_generation_engine,
        max_results: int = 5,
    ):
        """
        Initialise the Application Engine.

        Parameters
        ----------
        providers
            Document providers used to load heritage knowledge.

        chunking_engine
            Converts documents into smaller searchable chunks.

        embedding_engine
            Converts text into semantic vector representations.

        vector_database_engine
            Stores vectors and performs semantic similarity search.

        retrieval_policy_engine
            Determines which retrieved chunks are relevant enough
            to continue through the pipeline.

        context_engine
            Converts approved chunks into one LLM-ready context.

        response_generation_engine
            Generates the grounded natural-language answer.

        max_results
            Maximum number of candidate chunks requested during
            retrieval.
        """

        if not providers:
            raise ValueError(
                "At least one knowledge provider is required."
            )

        if chunking_engine is None:
            raise ValueError(
                "A Chunking Engine is required."
            )

        if embedding_engine is None:
            raise ValueError(
                "An Embedding Engine is required."
            )

        if vector_database_engine is None:
            raise ValueError(
                "A Vector Database Engine is required."
            )

        if retrieval_policy_engine is None:
            raise ValueError(
                "A Retrieval Policy Engine is required."
            )

        if context_engine is None:
            raise ValueError(
                "A Context Engine is required."
            )

        if response_generation_engine is None:
            raise ValueError(
                "A Response Generation Engine is required."
            )

        if max_results <= 0:
            raise ValueError(
                "max_results must be greater than zero."
            )

        self.providers = providers
        self.chunking_engine = chunking_engine
        self.embedding_engine = embedding_engine
        self.vector_database_engine = vector_database_engine
        self.retrieval_policy_engine = retrieval_policy_engine
        self.context_engine = context_engine
        self.response_generation_engine = (
            response_generation_engine
        )
        self.max_results = max_results

        # RetrievalEngine owns the complete knowledge retrieval flow.
        #
        # It receives the same proven dependencies that were used in
        # previous releases.
        self.retrieval_engine = RetrievalEngine(
            providers=self.providers,
            chunking_engine=self.chunking_engine,
            embedding_engine=self.embedding_engine,
            vector_database_engine=self.vector_database_engine,
            retrieval_policy_engine=(
                self.retrieval_policy_engine
            ),
            max_results=self.max_results,
        )

        self.is_prepared = False

    def prepare(self) -> int:
        """
        Prepare the heritage knowledge base.

        This startup operation should run once when the application
        launches.

        Startup flow:

        Providers
            ↓
        Heritage Documents
            ↓
        Chunking Engine
            ↓
        Heritage Chunks
            ↓
        Embedding Engine
            ↓
        Embedded Chunks
            ↓
        Vector Database Engine
            ↓
        Searchable Semantic Index

        Returns
        -------
        int
            Number of heritage chunks indexed.
        """

        indexed_chunk_count = self.retrieval_engine.prepare()

        self.is_prepared = True

        return indexed_chunk_count

    def ask(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """
        Answer a heritage question using the complete RAG pipeline.

        Parameters
        ----------
        query
            The user's heritage question.

        Returns
        -------
        dict
            Stable application result containing:

            - query
            - answer
            - context
            - result_count
            - results
            - message
        """

        clean_query = (query or "").strip()

        if not clean_query:
            return self._build_result(
                query="",
                answer="",
                context="",
                results=[],
                message="Please enter a heritage question.",
            )

        if not self.is_prepared:
            return self._build_result(
                query=clean_query,
                answer="",
                context="",
                results=[],
                message=(
                    "The heritage knowledge base has not been "
                    "prepared."
                ),
            )

        # =========================================================
        # STEP 1 - RETRIEVE APPROVED KNOWLEDGE
        # =========================================================
        #
        # RetrievalEngine performs:
        #
        # Query
        #   ↓
        # Query Embedding
        #   ↓
        # Vector Search
        #   ↓
        # Candidate Chunks
        #   ↓
        # Retrieval Policy
        #   ↓
        # Approved Chunks
        # =========================================================

        approved_chunks = self.retrieval_engine.retrieve(
            query=clean_query,
        )

        if not approved_chunks:
            fallback_answer = (
                "The available heritage documents do not contain "
                "enough information to answer this question."
            )

            return self._build_result(
                query=clean_query,
                answer=fallback_answer,
                context="",
                results=[],
                message=(
                    "No sufficiently relevant heritage knowledge "
                    "was found."
                ),
            )

        # =========================================================
        # STEP 2 - BUILD LLM-READY CONTEXT
        # =========================================================

        context = self.context_engine.build_context(
            approved_chunks=approved_chunks,
        )

        if not context.strip():
            fallback_answer = (
                "The available heritage documents do not contain "
                "enough information to answer this question."
            )

            return self._build_result(
                query=clean_query,
                answer=fallback_answer,
                context="",
                results=approved_chunks,
                message=(
                    "Relevant knowledge was retrieved, but no "
                    "usable context could be created."
                ),
            )

        # =========================================================
        # STEP 3 - GENERATE GROUNDED ANSWER
        # =========================================================

        answer = (
            self.response_generation_engine.generate_response(
                query=clean_query,
                context=context,
            )
        )

        return self._build_result(
            query=clean_query,
            answer=answer,
            context=context,
            results=approved_chunks,
            message=(
                f"Answer generated from "
                f"{len(approved_chunks)} approved heritage "
                f"source chunk(s)."
            ),
        )

    def search(
        self,
        query: str,
    ) -> Dict[str, Any]:
        """
        Preserve the earlier search contract for compatibility.

        This method retrieves approved chunks without generating
        an answer.

        It may be removed in a future release after all callers
        have migrated to ask().
        """

        clean_query = (query or "").strip()

        if not clean_query:
            return {
                "query": "",
                "result_count": 0,
                "results": [],
                "message": "Please enter a heritage question.",
            }

        if not self.is_prepared:
            return {
                "query": clean_query,
                "result_count": 0,
                "results": [],
                "message": (
                    "The heritage knowledge base has not been "
                    "prepared."
                ),
            }

        approved_chunks = self.retrieval_engine.retrieve(
            query=clean_query,
        )

        return {
            "query": clean_query,
            "result_count": len(approved_chunks),
            "results": approved_chunks,
            "message": (
                f"{len(approved_chunks)} approved heritage "
                f"chunk(s) found."
            ),
        }

    @staticmethod
    def _build_result(
        query: str,
        answer: str,
        context: str,
        results: List[Dict[str, Any]],
        message: str,
    ) -> Dict[str, Any]:
        """
        Build the stable result returned by ask().
        """

        return {
            "query": query,
            "answer": answer,
            "context": context,
            "result_count": len(results),
            "results": results,
            "message": message,
        }