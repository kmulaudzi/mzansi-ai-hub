"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 002 - Heritage Search Engine

Platform settings shared across the release.
"""

from pathlib import Path


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR
    / "foundation-dataset"
    / "knowledge-cards"
)

PDF_DATASET_PATH = (
    BASE_DIR
    / "foundation-dataset"
    / "pdfs"
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

CAPABILITY_NAME = "Heritage Intelligence Engine"

RELEASE_NAME = "Release 002 - Heritage Search Engine"


# -------------------------------------------------------------------
# Search Settings
# -------------------------------------------------------------------

MAX_RESULTS = 5

TITLE_WEIGHT = 3

CONTENT_WEIGHT = 1

# -------------------------------------------------------------------
# Embedding Settings
# -------------------------------------------------------------------

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

"""
Release 008
Retrieval Policies
"""

SIMILARITY_THRESHOLD = 0.50
# -------------------------------------------------------------
# Response Generation Settings
# -------------------------------------------------------------

RESPONSE_MODEL_NAME = "google/flan-t5-base"
MAX_RESPONSE_TOKENS = 200
# -------------------------------------------------------------------
# User Interface Settings
# -------------------------------------------------------------------

WINDOW_TITLE = "Heritage Search Engine"

SEARCH_LABEL = "Search Heritage Knowledge"

SEARCH_PLACEHOLDER = "Search South African heritage..."

RESULTS_LABEL = "Search Results"

APPLICATION_DESCRIPTION = (
    f"{RELEASE_NAME} of the {CAPABILITY_NAME}. "
    "Search and rank structured South African heritage Knowledge Cards."
)

