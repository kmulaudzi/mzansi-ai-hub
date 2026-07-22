"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 008 - Semantic Retrieval Engine

Capability Bootstrap
"""

from typing import Any

from application_engine import ApplicationEngine
from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.markdown_provider import MarkdownProvider
from providers.pdf_provider import PDFProvider
from retrieval_policy_engine import RetrievalPolicyEngine
from settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATASET_PATH,
    MAX_RESULTS,
    PDF_DATASET_PATH,
    SIMILARITY_THRESHOLD,
)
from vector_database_engine import VectorDatabaseEngine


def create_application(
    embedding_model: Any,
) -> ApplicationEngine:
    """
    Assemble and return the Semantic Retrieval application.

    Parameters
    ----------
    embedding_model:
        External embedding model used by the Embedding Engine.

    Returns
    -------
    ApplicationEngine
        Fully configured Semantic Retrieval application.

    Notes
    -----
    This function assembles the capability only.

    It does not:

    - prepare the knowledge index
    - perform a search
    - create a Gradio interface
    - launch the application
    """

    markdown_provider = MarkdownProvider(
        source_path=str(DATASET_PATH)
    )

    pdf_provider = PDFProvider(
        source_path=str(PDF_DATASET_PATH)
    )

    chunking_engine = ChunkingEngine(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    embedding_engine = EmbeddingEngine(
        model=embedding_model
    )

    vector_database_engine = VectorDatabaseEngine()

    retrieval_policy_engine = RetrievalPolicyEngine(
        similarity_threshold=SIMILARITY_THRESHOLD
    )

    return ApplicationEngine(
        providers=[
            markdown_provider,
            pdf_provider,
        ],
        chunking_engine=chunking_engine,
        embedding_engine=embedding_engine,
        vector_database_engine=vector_database_engine,
        retrieval_policy_engine=retrieval_policy_engine,
        max_results=MAX_RESULTS,
    )