"""
Mzansi AI Hub
Heritage Intelligence Engine

Response Generation Capability

Response Generation Engine
"""

from typing import Dict, List

from capabilities.response_generation.providers.base_generation_provider import (
    BaseGenerationProvider,
)


class ResponseGenerationEngine:
    """
    Generate a grounded response from a question and evidence.

    Responsibilities
    ----------------
    - Build grounded context from approved evidence.
    - Build the generation prompt.
    - Delegate generation to a Generation Provider.
    - Return the generated answer.

    It does not:
    - retrieve evidence
    - search FAISS
    - generate embeddings
    - read source documents directly
    - know how a specific model technology works
    """

    def __init__(
        self,
        generation_provider: BaseGenerationProvider,
    ):
        if generation_provider is None:
            raise ValueError(
                "generation_provider is required."
            )

        self.generation_provider = (
            generation_provider
        )

    def build_context(
        self,
        evidence: List[Dict],
    ) -> str:
        """
        Convert clean evidence into grounded context.
        """

        context_parts = []

        for index, item in enumerate(
            evidence,
            start=1,
        ):
            content = item.get(
                "content",
                "",
            ).strip()

            if not content:
                continue

            title = item.get(
                "title",
                "Unknown source",
            )

            similarity = item.get(
                "similarity",
                0.0,
            )

            context_parts.append(
                f"Evidence {index}\n"
                f"Source: {title}\n"
                f"Similarity: {similarity:.4f}\n"
                f"{content}"
            )

        return "\n\n".join(context_parts)

    def build_prompt(
        self,
        question: str,
        evidence: List[Dict],
    ) -> str:
        """
        Build a grounded prompt from the question
        and approved evidence.
        """

        context = self.build_context(
            evidence=evidence
        )

        if not context:
            return ""

        return (
            "You are a heritage knowledge assistant.\n\n"
            "Using only the evidence provided, write a clear, "
            "complete and informative answer to the question.\n"
            "Summarize the most important facts from the evidence.\n"
            "Do not answer with only a phrase or sentence fragment.\n"
            "Do not introduce facts that are not supported by "
            "the evidence.\n"
            "If the evidence is insufficient, say that the "
            "available evidence is insufficient.\n\n"
            f"Question:\n{question}\n\n"
            f"Evidence:\n{context}\n\n"
            "Complete answer:"
        )

    def generate(
        self,
        question: str,
        evidence: List[Dict],
    ) -> str:
        """
        Generate an answer grounded in supplied evidence.
        """

        # Keep the strongest evidence items for now.
        top_evidence = evidence[:3]

        prompt = self.build_prompt(
            question=question,
            evidence=top_evidence,
        )

        if not prompt:
            return (
                "I could not generate a grounded answer "
                "because no supporting evidence was provided."
            )

        return self.generation_provider.generate(
            prompt=prompt
        )