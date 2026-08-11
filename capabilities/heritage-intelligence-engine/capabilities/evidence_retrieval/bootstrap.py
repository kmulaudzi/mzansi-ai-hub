"""
Mzansi AI Hub
Heritage Intelligence Engine

Evidence Retrieval Capability

Capability Bootstrap
"""

from typing import Any

from .application import EvidenceRetrievalApplication
from .engines.evidence_retrieval_engine import (
    EvidenceRetrievalEngine,
)


def create_application(
    semantic_retrieval_application: Any,
) -> EvidenceRetrievalApplication:
    """
    Assemble and return the Evidence Retrieval application.

    Parameters
    ----------
    semantic_retrieval_application:
        Existing Semantic Retrieval application.

        Evidence Retrieval depends on Semantic Retrieval
        to find relevant, policy-approved knowledge.

    Returns
    -------
    EvidenceRetrievalApplication
        Fully assembled Evidence Retrieval capability.

    Notes
    -----
    This bootstrap only connects the capability dependencies.

    It does not:

    - prepare the semantic knowledge index
    - generate embeddings
    - perform retrieval
    - generate an AI response
    - create a user interface
    """

    evidence_retrieval_engine = EvidenceRetrievalEngine(
        semantic_retrieval_application=(
            semantic_retrieval_application
        )
    )

    return EvidenceRetrievalApplication(
        evidence_retrieval_engine=(
            evidence_retrieval_engine
        )
    )