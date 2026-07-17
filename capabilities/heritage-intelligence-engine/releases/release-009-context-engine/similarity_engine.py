"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 006 - Semantic Search Engine

Similarity Engine
"""

from copy import deepcopy
from typing import Dict, List

from sentence_transformers.util import cos_sim


class SimilarityEngine:
    """
    Compare a query embedding against cached document embeddings.

    Responsibility
    --------------
    Calculate cosine similarity between a user's query and every
    embedded heritage chunk.

    This engine is stateless.

    It does not:
        - Learn
        - Store information
        - Train
        - Predict

    It simply measures semantic similarity.
    """

    def compare(
        self,
        query_embedding,
        embedded_chunks: List[Dict],
    ) -> List[Dict]:
        """
        Compare one query embedding against all embedded chunks.

        Parameters
        ----------
        query_embedding
            Vector representing the user's question.

        embedded_chunks
            Cached chunks that already contain embeddings.

        Returns
        -------
        List[Dict]

            Original chunks enriched with a similarity score,
            sorted from highest similarity to lowest similarity.
        """

        results = []

        for chunk in embedded_chunks:

            similarity_score = cos_sim(
                query_embedding,
                chunk["embedding"],
            ).item()

            enriched_chunk = deepcopy(chunk)

            enriched_chunk["similarity"] = similarity_score

            results.append(
                enriched_chunk
            )

        results.sort(
            key=lambda chunk: chunk["similarity"],
            reverse=True,
        )

        return results