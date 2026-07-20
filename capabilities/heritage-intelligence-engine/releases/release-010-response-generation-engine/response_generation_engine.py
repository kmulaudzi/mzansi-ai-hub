"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine

Knowledge Communication Capability
"""

from typing import Any

from settings import (
    DO_SAMPLE,
    MAX_NEW_TOKENS,
    SYSTEM_PROMPT,
    TEMPERATURE,
)


class ResponseGenerationEngine:
    """
    Convert prepared heritage context into a grounded answer.

    This engine is responsible only for:

    - validating the question and context
    - building a controlled prompt
    - invoking the injected language model
    - decoding and returning the answer

    It does not retrieve documents, build embeddings,
    construct context, or manage the user interface.
    """

    def __init__(
        self,
        model: Any,
        tokenizer: Any,
        max_new_tokens: int = MAX_NEW_TOKENS,
        temperature: float = TEMPERATURE,
        do_sample: bool = DO_SAMPLE,
    ):
        """
        Connect a language model and tokenizer to the engine.

        Parameters
        ----------
        model : Any
            A model exposing a generate() method.

        tokenizer : Any
            A tokenizer that can encode text and decode model output.

        max_new_tokens : int
            Maximum number of tokens generated for one answer.

        temperature : float
            Sampling temperature used only when sampling is enabled.

        do_sample : bool
            Whether generation should use sampling.
        """

        if model is None:
            raise ValueError(
                "ResponseGenerationEngine requires a model."
            )

        if tokenizer is None:
            raise ValueError(
                "ResponseGenerationEngine requires a tokenizer."
            )

        if not hasattr(model, "generate"):
            raise TypeError(
                "The model must provide a generate() method."
            )

        if not callable(tokenizer):
            raise TypeError(
                "The tokenizer must be callable."
            )

        if not hasattr(tokenizer, "decode"):
            raise TypeError(
                "The tokenizer must provide a decode() method."
            )

        if max_new_tokens <= 0:
            raise ValueError(
                "max_new_tokens must be greater than zero."
            )

        if temperature < 0:
            raise ValueError(
                "temperature cannot be negative."
            )

        self.model = model
        self.tokenizer = tokenizer
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.do_sample = do_sample

    def generate_response(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Generate one grounded answer.

        Parameters
        ----------
        query : str
            User's heritage question.

        context : str
            Prepared context supplied by the Context Engine.

        Returns
        -------
        str
            Grounded natural-language answer.
        """

        clean_query = (query or "").strip()
        clean_context = (context or "").strip()

        if not clean_query:
            raise ValueError(
                "The query must not be empty."
            )

        if not clean_context:
            return (
                "The available heritage knowledge does not contain "
                "enough information to answer this question."
            )

        prompt = self._build_prompt(
            query=clean_query,
            context=clean_context,
        )

        model_inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
        )

        generation_arguments = {
            "max_new_tokens": self.max_new_tokens,
            "do_sample": self.do_sample,
        }

        if self.do_sample:
            generation_arguments["temperature"] = self.temperature

        generated_tokens = self.model.generate(
            **model_inputs,
            **generation_arguments,
        )

        answer = self.tokenizer.decode(
            generated_tokens[0],
            skip_special_tokens=True,
        ).strip()

        if not answer:
            return (
                "The available heritage knowledge does not contain "
                "enough information to answer this question."
            )

        return answer

    @staticmethod
    def _build_prompt(
        query: str,
        context: str,
    ) -> str:
        """
        Build the controlled grounding prompt.

        The prompt policy is stored in settings.py so it can evolve
        independently from the engine implementation.
        """

        return SYSTEM_PROMPT.format(
            question=query,
            context=context,
        )