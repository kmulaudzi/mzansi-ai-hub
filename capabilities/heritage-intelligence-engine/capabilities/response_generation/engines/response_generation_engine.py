"""
Mzansi AI Hub
Heritage Intelligence Engine

Response Generation Capability

Response Generation Engine
"""

from typing import Any, Dict, List


class ResponseGenerationEngine:
    """
    Generate a grounded response from a question and evidence.

    Responsibilities
    ----------------
    - Build model-ready context from approved evidence.
    - Send the grounded prompt to the generation model.
    - Return the generated answer.

    It does not:
    - retrieve evidence
    - search FAISS
    - generate embeddings
    - read source documents directly
    """

    def __init__(
        self,
        model: Any,
        tokenizer: Any,
    ):
        if model is None:
            raise ValueError("model is required.")

        if tokenizer is None:
            raise ValueError("tokenizer is required.")

        self.model = model
        self.tokenizer = tokenizer

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

            context_parts.append(
                f"Evidence {index}\n"
                f"Source: {title}\n"
                f"{content}"
            )

        return "\n\n".join(context_parts)

    def generate(
        self,
        question: str,
        evidence: List[Dict],
    ) -> str:
        """
        Generate an answer grounded in supplied evidence.
        """

        context = self.build_context(
            evidence=evidence
        )

        if not context:
            return (
                "I could not generate a grounded answer "
                "because no supporting evidence was provided."
            )

        prompt = (
            "Answer the question using only the evidence below.\n"
            "If the evidence is insufficient, say that the available "
            "evidence is insufficient.\n\n"
            f"Question:\n{question}\n\n"
            f"Evidence:\n{context}\n\n"
            "Answer:"
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
        )

        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        )

        return answer.strip()