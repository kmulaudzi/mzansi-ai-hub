"""
Mzansi AI Hub
Heritage Intelligence Engine

Response Generation Capability

Capability Bootstrap
"""

from typing import Any

from .application import (
    ResponseGenerationApplication,
)
from .engines.response_generation_engine import (
    ResponseGenerationEngine,
)
from .providers.huggingface_generation_provider import (
    HuggingFaceGenerationProvider,
)


def create_application(
    model: Any,
    tokenizer: Any,
    max_new_tokens: int = 250,
) -> ResponseGenerationApplication:
    """
    Assemble and return the Response Generation application.

    Parameters
    ----------
    model:
        External Hugging Face generation model.

    tokenizer:
        Tokenizer paired with the generation model.

    max_new_tokens:
        Maximum number of new tokens the provider
        may generate for a response.

    Returns
    -------
    ResponseGenerationApplication
        Fully assembled Response Generation capability.

    Notes
    -----
    This bootstrap assembles the capability only.

    It does not:

    - retrieve evidence
    - prepare semantic retrieval
    - load source documents
    - launch a user interface

    Runtime assembly
    ----------------
    Hugging Face model + tokenizer
            ↓
    HuggingFaceGenerationProvider
            ↓
    ResponseGenerationEngine
            ↓
    ResponseGenerationApplication
    """

    generation_provider = (
        HuggingFaceGenerationProvider(
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
        )
    )

    response_generation_engine = (
        ResponseGenerationEngine(
            generation_provider=generation_provider
        )
    )

    return ResponseGenerationApplication(
        response_generation_engine=(
            response_generation_engine
        )
    )