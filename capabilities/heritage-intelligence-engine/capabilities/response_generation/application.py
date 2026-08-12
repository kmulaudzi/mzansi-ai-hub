"""
Mzansi AI Hub
Heritage Intelligence Engine

Response Generation Capability

Public Application Interface
"""

from typing import Dict, List

from .engines.response_generation_engine import (
    ResponseGenerationEngine,
)


class ResponseGenerationApplication:
    """
    Public interface for the Response Generation capability.

    Public method
    -------------
    generate(question, evidence)
        Generate a grounded answer from approved evidence.
    """

    def __init__(
        self,
        response_generation_engine: ResponseGenerationEngine,
    ):
        if response_generation_engine is None:
            raise ValueError(
                "response_generation_engine is required."
            )

        self.response_generation_engine = (
            response_generation_engine
        )

    def generate(
        self,
        question: str,
        evidence: List[Dict],
    ) -> Dict:
        """
        Generate a grounded response.

        Parameters
        ----------
        question:
            User question.

        evidence:
            Clean evidence produced by the
            Evidence Retrieval capability.
        """

        clean_question = question.strip()

        if not clean_question:
            return {
                "success": False,
                "capability": "Response Generation",
                "question": "",
                "answer": "",
                "evidence_count": 0,
                "message": "Please enter a question.",
            }

        if not evidence:
            return {
                "success": True,
                "capability": "Response Generation",
                "question": clean_question,
                "answer": (
                    "I could not generate a grounded answer "
                    "because no supporting evidence was found."
                ),
                "evidence_count": 0,
                "message": "No evidence available.",
            }

        answer = (
            self.response_generation_engine.generate(
                question=clean_question,
                evidence=evidence,
            )
        )

        return {
            "success": True,
            "capability": "Response Generation",
            "question": clean_question,
            "answer": answer,
            "evidence_count": len(evidence),
            "message": "Grounded response generated.",
        }