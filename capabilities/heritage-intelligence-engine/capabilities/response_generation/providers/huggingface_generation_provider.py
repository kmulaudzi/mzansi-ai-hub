"""
Mzansi AI Hub
Heritage Intelligence Engine

Response Generation Capability

Hugging Face Generation Provider
"""

from typing import Any

from .base_generation_provider import (
    BaseGenerationProvider,
)


class HuggingFaceGenerationProvider(
    BaseGenerationProvider
):
    """
    Generation provider backed by a Hugging Face model.

    Responsibilities
    ----------------
    - Tokenize the prompt.
    - Move model inputs to the model device.
    - Call the Hugging Face generation model.
    - Separate prompt tokens from newly generated tokens
      for causal language models.
    - Decode generated tokens.
    - Hide Hugging Face-specific behaviour from the
      Response Generation Engine.

    The Response Generation Engine only knows:

        provider.generate(prompt)
    """

    def __init__(
        self,
        model: Any,
        tokenizer: Any,
        max_new_tokens: int = 250,
    ):
        if model is None:
            raise ValueError("model is required.")

        if tokenizer is None:
            raise ValueError("tokenizer is required.")

        if max_new_tokens <= 0:
            raise ValueError(
                "max_new_tokens must be greater than zero."
            )

        self.model = model
        self.tokenizer = tokenizer
        self.max_new_tokens = max_new_tokens

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate text from a grounded prompt.
        """

        clean_prompt = prompt.strip()

        if not clean_prompt:
            return ""

        # ---------------------------------------------------------
        # Tokenize
        # ---------------------------------------------------------

        inputs = self.tokenizer(
            clean_prompt,
            return_tensors="pt",
            truncation=True,
        )

        # ---------------------------------------------------------
        # Move inputs to the same device as the model.
        #
        # This matters when Colab loads the model onto a GPU.
        # ---------------------------------------------------------

        model_device = next(
            self.model.parameters()
        ).device

        inputs = {
            key: value.to(model_device)
            for key, value in inputs.items()
        }

        # ---------------------------------------------------------
        # Generate
        # ---------------------------------------------------------

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            do_sample=False,
        )

        # ---------------------------------------------------------
        # Determine model architecture.
        #
        # Encoder-decoder:
        #     output = generated answer
        #
        # Causal language model:
        #     output = input prompt + generated answer
        # ---------------------------------------------------------

        is_encoder_decoder = getattr(
            self.model.config,
            "is_encoder_decoder",
            False,
        )

        if is_encoder_decoder:

            generated_tokens = outputs[0]

        else:

            input_token_count = inputs[
                "input_ids"
            ].shape[-1]

            generated_tokens = outputs[
                0,
                input_token_count:
            ]

        # ---------------------------------------------------------
        # Decode ONLY the generated response.
        # ---------------------------------------------------------

        answer = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        return answer.strip()