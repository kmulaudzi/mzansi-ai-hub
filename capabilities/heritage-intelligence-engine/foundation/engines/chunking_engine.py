"""
Mzansi AI Hub
Heritage Intelligence Engine

Foundation

Document Chunking Engine
"""

from typing import Dict, List


class ChunkingEngine:
    """
    Split standardized documents into smaller
    searchable knowledge chunks.

    The engine preserves source metadata while
    adding chunk-specific metadata.
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
                "chunk_overlap must be smaller "
                "than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_documents(
        self,
        documents: List[Dict],
    ) -> List[Dict]:
        """
        Split standardized documents into chunks.

        Parameters
        ----------
        documents:
            Documents supplied by one or more providers.

        Returns
        -------
        List[Dict]
            Searchable chunks with preserved source
            metadata and chunk-specific metadata.
        """

        chunks = []

        for document in documents:

            content = document.get(
                "content",
                "",
            ).strip()

            if not content:
                continue

            document_chunks = self._split_text(
                content
            )

            for chunk_index, chunk_content in enumerate(
                document_chunks
            ):
                chunk = document.copy()

                chunk["content"] = chunk_content

                chunk["chunk_index"] = chunk_index

                # -------------------------------------------------
                # Build a unique chunk identifier.
                #
                # Markdown documents normally have no page number:
                #
                # mapungubwe_kingdom.md-chunk-0
                #
                # PDF documents now preserve page boundaries:
                #
                # heritage.pdf-page-7-chunk-0
                # -------------------------------------------------

                page_number = document.get(
                    "page_number"
                )

                if page_number is not None:

                    chunk["chunk_id"] = (
                        f"{document['filename']}"
                        f"-page-{page_number}"
                        f"-chunk-{chunk_index}"
                    )

                else:

                    chunk["chunk_id"] = (
                        f"{document['filename']}"
                        f"-chunk-{chunk_index}"
                    )

                chunk["parent_document"] = (
                    document["filename"]
                )

                chunks.append(chunk)

        return chunks

    def _split_text(
        self,
        text: str,
    ) -> List[str]:
        """
        Split one document using character-based
        overlapping chunks.

        Source boundaries such as PDF pages are already
        preserved by the Provider before this method runs.
        """

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk = text[
                start:end
            ].strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks