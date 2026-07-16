"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 006 - Semantic Search Engine

Embedding Engine
"""

from typing import Any, Dict, List


class EmbeddingEngine:
    """
    Converts text into vector representations.

    The engine receives an embedding model through dependency injection.
    It does not create or download the model itself.

    Release 006 capabilities
    ------------------------
    - embed_chunks():
      Used during application startup to embed document chunks.

    - embed_text():
      Used during search time to embed the user's query.
    """

    def __init__(self, model: Any):
        """
        Connect an external embedding model to our architecture.

        Parameters
        ----------
        model : Any
            Any model that exposes an encode() method.
        """

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

        This method is used during application startup.

        Parameters
        ----------
        chunks : List[Dict]
            Document chunks containing text in the content field.

        Returns
        -------
        List[Dict]
            Copies of the original chunks with:
            - embedding
            - embedding_dimension
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

    def embed_text(
        self,
        text: str,
    ) -> List[float]:
        """
        Convert one piece of text into one embedding vector.

        This method is used during search time.

        Examples
        --------
        - User query
        - Question
        - Search phrase
        - Any single text value

        Parameters
        ----------
        text : str
            Text to convert into an embedding.

        Returns
        -------
        List[float]
            One embedding vector represented as a plain Python list.
        """

        clean_text = text.strip()

        if not clean_text:
            raise ValueError(
                "Text must not be empty."
            )

        vector = self.model.encode(
            clean_text
        )

        return self._to_list(
            vector
        )

    @staticmethod
    def _to_list(
        vector: Any,
    ) -> List[float]:
        """
        Convert an embedding vector into a plain Python list.

        This keeps the rest of the platform independent from whether
        the external model returns NumPy arrays, tensors, or lists.
        """

        if hasattr(vector, "tolist"):
            vector = vector.tolist()

        return [
            float(value)
            for value in vector
        ]