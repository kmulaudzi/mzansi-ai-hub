"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 008 - Retrieval Policy Engine
"""

from copy import deepcopy
from typing import Dict, List


class RetrievalPolicyEngine:
    """
    Applies retrieval policies to candidate heritage chunks.

    Current policy
    --------------
    Similarity threshold.
    """

    def __init__(
        self,
        similarity_threshold: float,
    ):
        if not (
            0.0 <= similarity_threshold <= 1.0
        ):
            raise ValueError(
                "similarity_threshold must "
                "be between 0 and 1."
            )

        self.similarity_threshold = (
            similarity_threshold
        )

    def apply(
        self,
        candidate_chunks: List[Dict],
    ) -> List[Dict]:
        """
        Apply every retrieval policy.

        Current Release
        ---------------
        Keep only chunks whose similarity
        is greater than or equal to the
        configured threshold.
        """

        approved_chunks = []

        for chunk in candidate_chunks:

            similarity = chunk.get(
                "similarity",
                0.0,
            )

            if similarity >= self.similarity_threshold:

                approved_chunks.append(
                    deepcopy(chunk)
                )

        return approved_chunks