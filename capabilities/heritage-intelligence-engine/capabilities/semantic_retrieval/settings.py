"""
Mzansi AI Hub
Heritage Intelligence Engine

Semantic Retrieval Capability Settings

Central configuration for dataset paths, chunking,
embeddings, retrieval, and application information.
"""

from pathlib import Path


# -------------------------------------------------------------------
# Repository Paths
# -------------------------------------------------------------------

# Current file:
# heritage-intelligence-engine/
#     capabilities/
#         semantic_retrieval/
#             settings.py

CAPABILITY_DIR = Path(__file__).resolve().parent

# heritage-intelligence-engine/
ENGINE_ROOT = CAPABILITY_DIR.parents[1]

# heritage-intelligence-engine/datasets/
DATASETS_DIR = ENGINE_ROOT / "datasets"


def first_existing_path(*paths: Path) -> Path:
    """
    Return the first path that currently exists.

    If none exist, return the first configured path so that any later
    error message still shows the preferred repository location.
    """

    for path in paths:
        if path.exists():
            return path

    return paths[0]


# Support the likely dataset layouts while the repository is being
# reorganised.

DATASET_PATH = first_existing_path(
    DATASETS_DIR / "knowledge-cards",
    DATASETS_DIR / "knowledge_cards",
    DATASETS_DIR / "foundation-dataset" / "knowledge-cards",
    DATASETS_DIR / "foundation_dataset" / "knowledge_cards",
)

PDF_DATASET_PATH = first_existing_path(
    DATASETS_DIR / "pdfs",
    DATASETS_DIR / "foundation-dataset" / "pdfs",
    DATASETS_DIR / "foundation_dataset" / "pdfs",
)


# -------------------------------------------------------------------
# Chunking Settings
# -------------------------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200


# -------------------------------------------------------------------
# Application Information
# -------------------------------------------------------------------

APPLICATION_NAME = "Mzansi AI Hub"

CAPABILITY_NAME = "Semantic Retrieval"

ENGINE_NAME = "Heritage Intelligence Engine"


# -------------------------------------------------------------------
# Search Settings
# -------------------------------------------------------------------

MAX_RESULTS = 5

TITLE_WEIGHT = 3

CONTENT_WEIGHT = 1


# -------------------------------------------------------------------
# Embedding Settings
# -------------------------------------------------------------------

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------------------------------------------------------
# Retrieval Policies
# -------------------------------------------------------------------

SIMILARITY_THRESHOLD = 0.50


# -------------------------------------------------------------------
# User Interface Settings
# -------------------------------------------------------------------

WINDOW_TITLE = "Heritage Semantic Retrieval"

SEARCH_LABEL = "Search Heritage Knowledge"

SEARCH_PLACEHOLDER = "Search South African heritage..."

RESULTS_LABEL = "Search Results"

APPLICATION_DESCRIPTION = (
    f"{CAPABILITY_NAME} capability of the "
    f"{ENGINE_NAME}. Search structured South African "
    "heritage knowledge using semantic similarity."
)