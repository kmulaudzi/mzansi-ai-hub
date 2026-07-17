"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 009 - Context Engine
"""

from typing import Dict, List


class ContextEngine:
    """
    Converts approved heritage chunks into one LLM-ready
    context string.

    Responsibility
    --------------
    The Context Engine organizes approved knowledge.

    It does not:
    - retrieve documents
    - generate embeddings
    - apply retrieval policies
    - answer the user's question
    - call an LLM
    """

    def build_context(
        self,
        approved_chunks: List[Dict],
    ) -> str:
        """
        Build an LLM-ready context string.

        Parameters
        ----------
        approved_chunks : List[Dict]
            Heritage chunks approved by the
            Retrieval Policy Engine.

        Returns
        -------
        str
            One formatted context string.
        """

        if not approved_chunks:
            return ""

        context_sections = []

        for position, chunk in enumerate(
            approved_chunks,
            start=1,
        ):
            title = str(
                chunk.get("title", "Unknown Source")
            ).strip()

            content = str(
                chunk.get("content", "")
            ).strip()

            if not content:
                continue

            source = chunk.get("source", "")
            similarity = chunk.get("similarity")

            section_lines = [
                f"Context Item {position}",
                f"Title: {title}",
            ]

            if source:
                section_lines.append(
                    f"Source: {source}"
                )

            if similarity is not None:
                section_lines.append(
                    f"Similarity: {similarity:.4f}"
                )

            section_lines.extend(
                [
                    "",
                    content,
                ]
            )

            context_sections.append(
                "\n".join(section_lines)
            )

        return "\n\n---\n\n".join(
            context_sections
        ) 