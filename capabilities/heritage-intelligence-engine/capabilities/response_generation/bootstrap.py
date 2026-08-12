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


def create_application(
    model: Any,
    tokenizer: Any,
) -> ResponseGenerationApplication:
    """
    Assemble and return the Response Generation application.

    Parameters
    ----------
    model:
        External Hugging Face generation model.

    tokenizer:
        Tokenizer paired with the generation model.

    Returns
    -------
    ResponseGenerationApplication
        Fully assembled Response Generation capability.

    Notes
    -----
    This bootstrap only assembles dependencies.

    It does not:

    - retrieve evidence
    - prepare semantic retrieval
    - load source documents
    - launch a user interface
    """

    response_generation_engine = (
        ResponseGenerationEngine(
            model=model,
            tokenizer=tokenizer,
        )
    )

    return ResponseGenerationApplication(
        response_generation_engine=(
            response_generation_engine
        )
    )