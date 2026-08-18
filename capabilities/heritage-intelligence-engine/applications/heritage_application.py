"""
Mzansi AI Hub
Heritage Intelligence Engine

Heritage Application

Top-level application contract for interacting with
the Heritage Intelligence Engine.
"""

from typing import Any, Dict


class HeritageApplication:
    """
    Coordinate the Heritage Intelligence capabilities.

    Responsibilities
    ----------------
    - Prepare the heritage knowledge base.
    - Accept heritage questions.
    - Coordinate evidence retrieval.
    - Coordinate grounded response generation.
    - Return one clean application response.

    It does not:
    - read PDFs directly
    - create embeddings directly
    - search FAISS directly
    - execute language models directly

    Those responsibilities belong to the capabilities
    and foundation engines below this application.
    """

    def __init__(
        self,
        semantic_retrieval_application: Any,
        evidence_retrieval_application: Any,
        response_generation_application: Any,
    ):
        if semantic_retrieval_application is None:
            raise ValueError(
                "semantic_retrieval_application is required."
            )

        if evidence_retrieval_application is None:
            raise ValueError(
                "evidence_retrieval_application is required."
            )

        if response_generation_application is None:
            raise ValueError(
                "response_generation_application is required."
            )

        self.semantic_retrieval_application = (
            semantic_retrieval_application
        )

        self.evidence_retrieval_application = (
            evidence_retrieval_application
        )

        self.response_generation_application = (
            response_generation_application
        )

    def prepare(self) -> int:
        """
        Prepare the heritage knowledge base.

        This loads the configured source documents,
        chunks them, creates embeddings, and prepares
        the semantic retrieval index.

        Returns
        -------
        int
            Number of prepared knowledge chunks.
        """

        return self.semantic_retrieval_application.prepare()

    def ask(
        self,
        question: str,
    ) -> Dict:
        """
        Answer a heritage question using grounded evidence.
        """

        clean_question = question.strip()

        if not clean_question:
            raise ValueError(
                "question cannot be empty."
            )

        # ---------------------------------------------------------
        # STEP 1
        # Retrieve approved heritage evidence.
        # ---------------------------------------------------------

        evidence_response = (
            self.evidence_retrieval_application.retrieve(
                clean_question
            )
        )

        evidence = evidence_response.get(
            "evidence",
            [],
        )

        # ---------------------------------------------------------
        # STEP 2
        # Generate a response grounded in that evidence.
        # ---------------------------------------------------------

        generation_response = (
            self.response_generation_application.generate(
                question=clean_question,
                evidence=evidence,
            )
        )

        # ---------------------------------------------------------
        # STEP 3
        # Return one clean application-level contract.
        #
        # Gradio and future applications should consume this
        # structure rather than communicating with individual
        # engines directly.
        # ---------------------------------------------------------

        return {
            "question": clean_question,
            "answer": generation_response.get(
                "answer",
                "",
            ),
            "sources": evidence,
            "evidence_count": len(evidence),
        }