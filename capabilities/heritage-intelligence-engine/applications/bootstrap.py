"""
Mzansi AI Hub
Heritage Intelligence Engine

Top-Level Application Bootstrap

Assembles the complete Heritage Intelligence application.
"""

from typing import Any

from applications.heritage_application import (
    HeritageApplication,
)

from capabilities.semantic_retrieval.bootstrap import (
    create_application as create_semantic_application,
)

from capabilities.evidence_retrieval.bootstrap import (
    create_application as create_evidence_application,
)

from capabilities.response_generation.bootstrap import (
    create_application as create_response_application,
)


def create_application(
    embedding_model: Any,
    generation_model: Any,
    generation_tokenizer: Any,
) -> HeritageApplication:
    """
    Assemble and return the complete Heritage Application.

    Parameters
    ----------
    embedding_model:
        External embedding model used by Semantic Retrieval.

    generation_model:
        External generation model used by Response Generation.

    generation_tokenizer:
        Tokenizer paired with the generation model.

    Returns
    -------
    HeritageApplication
        Fully assembled Heritage Intelligence application.

    Runtime assembly
    ----------------
    Embedding Model
        ↓
    Semantic Retrieval
        ↓
    Evidence Retrieval

    Generation Model + Tokenizer
        ↓
    Response Generation

    Evidence Retrieval
            +
    Response Generation
            ↓
    HeritageApplication
    """

    # ---------------------------------------------------------
    # Semantic Retrieval
    # ---------------------------------------------------------

    semantic_application = create_semantic_application(
        embedding_model=embedding_model
    )

    # ---------------------------------------------------------
    # Evidence Retrieval
    #
    # Evidence Retrieval depends on Semantic Retrieval.
    # ---------------------------------------------------------

    evidence_application = create_evidence_application(
        semantic_retrieval_application=semantic_application
    )

    # ---------------------------------------------------------
    # Response Generation
    #
    # Response Generation owns its generation provider
    # internally through its capability bootstrap.
    # ---------------------------------------------------------

    response_application = create_response_application(
        model=generation_model,
        tokenizer=generation_tokenizer,
    )

    # ---------------------------------------------------------
    # Heritage Application
    #
    # This becomes the public application contract.
    # ---------------------------------------------------------

    return HeritageApplication(
        semantic_retrieval_application=semantic_application,
        evidence_retrieval_application=evidence_application,
        response_generation_application=response_application,
    )