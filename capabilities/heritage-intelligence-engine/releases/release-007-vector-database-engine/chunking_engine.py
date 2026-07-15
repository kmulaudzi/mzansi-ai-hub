"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 004 - Document Chunking Engine
"""

from typing import Dict, List


class ChunkingEngine:
    """
    Splits large documents into smaller searchable chunks.

    The engine preserves the original document metadata
    while adding chunk-specific metadata.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than zero."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(
        self,
        documents: List[Dict],
    ) -> List[Dict]:
        """
        Split documents into smaller chunks.

        Parameters
        ----------
        documents : List[Dict]
            Documents supplied by one or more providers.

        Returns
        -------
        List[Dict]
            Document chunks with preserved source metadata.
        """

        chunks = []

        for document in documents:
            content = document.get("content", "").strip()

            if not content:
                continue

            document_chunks = self._split_text(content)

            for chunk_index, chunk_content in enumerate(
                document_chunks
            ):
                chunk = document.copy()

                chunk["content"] = chunk_content
                chunk["chunk_index"] = chunk_index
                chunk["chunk_id"] = (
                    f"{document['filename']}"
                    f"-chunk-{chunk_index}"
                )
                chunk["parent_document"] = document["filename"]

                chunks.append(chunk)

        return chunks

    def _split_text(self, text: str) -> List[str]:
        """
        Split one text value using character-based chunking.
        """

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks