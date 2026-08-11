"""
Mzansi AI Hub
Heritage Intelligence Engine

Evidence Retrieval Capability

Public Application Interface
"""

from typing import Dict

from .engines.evidence_retrieval_engine import (
    EvidenceRetrievalEngine,
)


class EvidenceRetrievalApplication:
    """
    Public interface for the Evidence Retrieval capability.

    Public methods
    --------------
    prepare()
        Prepare the underlying Semantic Retrieval capability.

    retrieve(question)
        Return clean supporting evidence for a question.
    """

    def __init__(
        self,
        evidence_retrieval_engine: EvidenceRetrievalEngine,
    ):
        if evidence_retrieval_engine is None:
            raise ValueError(
                "evidence_retrieval_engine is required."
            )

        self.evidence_retrieval_engine = (
            evidence_retrieval_engine
        )

    def prepare(self) -> int:
        """
        Prepare the underlying Semantic Retrieval capability.
        """

        semantic_application = (
            self.evidence_retrieval_engine
            .semantic_retrieval_application
        )

        if not hasattr(
            semantic_application,
            "prepare",
        ):
            raise TypeError(
                "Semantic Retrieval application must "
                "provide a prepare() method."
            )

        return semantic_application.prepare()

    def retrieve(
        self,
        question: str,
    ) -> Dict:
        """
        Retrieve supporting evidence for a user question.
        """

        clean_question = question.strip()

        if not clean_question:
            return {
                "success": False,
                "capability": "Evidence Retrieval",
                "question": "",
                "evidence_count": 0,
                "evidence": [],
                "message": "Please enter a question.",
            }

        evidence = (
            self.evidence_retrieval_engine.retrieve(
                question=clean_question
            )
        )

        if not evidence:
            return {
                "success": True,
                "capability": "Evidence Retrieval",
                "question": clean_question,
                "evidence_count": 0,
                "evidence": [],
                "message": (
                    "No supporting heritage evidence "
                    "was found."
                ),
            }

        return {
            "success": True,
            "capability": "Evidence Retrieval",
            "question": clean_question,
            "evidence_count": len(evidence),
            "evidence": evidence,
            "message": (
                f"{len(evidence)} supporting "
                "evidence item(s) retrieved."
            ),
        }