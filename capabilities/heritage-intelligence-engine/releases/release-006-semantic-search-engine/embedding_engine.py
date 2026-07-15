"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 005 - Embedding Engine
"""

from typing import Any, Dict, List


class EmbeddingEngine:
    """
    Converts text chunks into vector representations.

    The engine receives an embedding model through dependency injection.
    It does not create or download the model itself.
    """

    def __init__(self, model: Any):
        if model is None:
            raise ValueError(
                "EmbeddingEngine requires an embedding model."
            )

        if not hasattr(model, "encode"):
            raise TypeError(
                "The embedding model must provide an encode() method."
            )

        self.model = model

    def embed_chunks(
        self,
        chunks: List[Dict],
    ) -> List[Dict]:
        """
        Convert document chunks into embedded chunks.

        Parameters
        ----------
        chunks : List[Dict]
            Document chunks containing text in the content field.

        Returns
        -------
        List[Dict]
            Copies of the original chunks with an embedding field added.
        """

        valid_chunks = [
            chunk
            for chunk in chunks
            if chunk.get("content", "").strip()
        ]

        if not valid_chunks:
            return []

        texts = [
            chunk["content"]
            for chunk in valid_chunks
        ]

        vectors = self.model.encode(texts)

        if len(vectors) != len(valid_chunks):
            raise ValueError(
                "The embedding model returned an unexpected "
                "number of vectors."
            )

        embedded_chunks = []

        for chunk, vector in zip(
            valid_chunks,
            vectors,
        ):
            embedded_chunk = chunk.copy()

            embedded_chunk["embedding"] = self._to_list(
                vector
            )

            embedded_chunk["embedding_dimension"] = len(
                embedded_chunk["embedding"]
            )

            embedded_chunks.append(
                embedded_chunk
            )

        return embedded_chunks

    @staticmethod
    def _to_list(vector: Any) -> List[float]:
        """
        Convert an embedding vector into a plain Python list.
        """

        if hasattr(vector, "tolist"):
            vector = vector.tolist()

        return [
            float(value)
            for value in vector
        ]