"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine
"""

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)


class ResponseGenerationEngine:
    """
    Generates grounded responses from
    LLM-ready context.

    Responsibilities
    ----------------

    ✓ Build prompts

    ✓ Call the language model

    ✓ Return the generated response

    It does NOT

    ✗ Retrieve documents

    ✗ Build embeddings

    ✗ Build context

    ✗ Display Gradio UI
    """

    def __init__(
        self,
        model: AutoModelForSeq2SeqLM,
        tokenizer: AutoTokenizer,
    ):
        self.model = model
        self.tokenizer = tokenizer

    def generate_response(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate a grounded heritage answer.
        """

        prompt = self._build_prompt(
            query=query,
            context=context,
        )

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
        )

        return response.strip()

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Construct a grounded prompt.
        """

        return f"""
You are the Heritage Intelligence Engine.

Answer ONLY using the supplied heritage context.

If the answer is not contained in the context, reply:

The available heritage documents do not contain enough information.

Question:
{query}

Context:
{context}

Answer:
"""