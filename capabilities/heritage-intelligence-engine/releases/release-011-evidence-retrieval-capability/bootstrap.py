"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 011 - Evidence Retrieval Capability

Capability Bootstrap
"""

from typing import Any

from evidence_retrieval_application import (
    EvidenceRetrievalApplication,
)
from evidence_retrieval_engine import (
    EvidenceRetrievalEngine,
)

# Release 008
from release_008_semantic_retrieval_engine.bootstrap import (
    create_application as create_semantic_retrieval,
)


def create_application(
    embedding_model: Any,
) -> EvidenceRetrievalApplication:
    """
    Assemble and return the Evidence Retrieval capability.

    Parameters
    ----------
    embedding_model:
        External embedding model used by the Semantic Retrieval
        capability.

    Returns
    -------
    EvidenceRetrievalApplication
        Fully configured Evidence Retrieval capability.

    Notes
    -----
    This function assembles the capability only.

    It does not:

    - prepare the semantic index
    - retrieve evidence
    - generate responses
    - create a user interface
    """

    semantic_retrieval = create_semantic_retrieval(
        embedding_model=embedding_model,
    )

    evidence_engine = EvidenceRetrievalEngine(
        semantic_retrieval=semantic_retrieval,
    )

    return EvidenceRetrievalApplication(
        evidence_engine=evidence_engine,
    )