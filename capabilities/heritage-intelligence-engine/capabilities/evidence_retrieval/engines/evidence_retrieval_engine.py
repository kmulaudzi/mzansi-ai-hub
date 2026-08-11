"""
Mzansi AI Hub
Heritage Intelligence Engine

Evidence Retrieval Capability

Evidence Retrieval Engine
"""

from copy import deepcopy
from typing import Any, Dict, List


class EvidenceRetrievalEngine:
    """
    Retrieve clean supporting evidence from
    the Semantic Retrieval capability.

    Responsibilities
    ----------------
    - Call Semantic Retrieval.
    - Receive approved retrieval results.
    - Remove internal embedding/vector details.
    - Return clean evidence for downstream capabilities.

    It does not:
    - generate embeddings
    - search FAISS directly
    - generate natural-language answers
    """

    def __init__(
        self,
        semantic_retrieval_application: Any,
    ):
        if semantic_retrieval_application is None:
            raise ValueError(
                "semantic_retrieval_application is required."
            )

        if not hasattr(
            semantic_retrieval_application,
            "search",
        ):
            raise TypeError(
                "semantic_retrieval_application must "
                "provide a search() method."
            )

        self.semantic_retrieval_application = (
            semantic_retrieval_application
        )

    def retrieve(
        self,
        question: str,
    ) -> List[Dict]:
        """
        Retrieve supporting evidence for a question.
        """

        retrieval_response = (
            self.semantic_retrieval_application.search(
                question
            )
        )

        retrieval_results = retrieval_response.get(
            "results",
            [],
        )

        evidence = []

        for result in retrieval_results:
            evidence_item = {
                "title": result.get(
                    "title",
                    "",
                ),
                "content": result.get(
                    "content",
                    "",
                ),
                "filename": result.get(
                    "filename",
                    "",
                ),
                "source_type": result.get(
                    "source_type",
                    "",
                ),
                "source_path": result.get(
                    "source_path",
                    "",
                ),
                "parent_document": result.get(
                    "parent_document",
                    "",
                ),
                "chunk_id": result.get(
                    "chunk_id",
                    "",
                ),
                "chunk_index": result.get(
                    "chunk_index",
                ),
                "similarity": result.get(
                    "similarity",
                    0.0,
                ),
            }

            evidence.append(
                deepcopy(evidence_item)
            )

        return evidence