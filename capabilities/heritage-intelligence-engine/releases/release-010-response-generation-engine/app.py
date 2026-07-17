"""
Mzansi AI Hub

Heritage Intelligence Engine

Release 010B
Full RAG Integration

This file is the Composition Root of the application.

Its responsibilities are:

1. Create every dependency.
2. Connect every engine.
3. Prepare the knowledge base.
4. Launch the Gradio application.

No business logic belongs here.
"""

from pathlib import Path

import gradio as gr

from sentence_transformers import SentenceTransformer

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from application_engine import ApplicationEngine

from chunking_engine import ChunkingEngine

from context_engine import ContextEngine

from embedding_engine import EmbeddingEngine

from providers.markdown_provider import MarkdownProvider
from providers.pdf_provider import PDFProvider

from response_generation_engine import (
    ResponseGenerationEngine,
)

from retrieval_policy_engine import (
    RetrievalPolicyEngine,
)

from settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    MAX_RESPONSE_TOKENS,
    MAX_RESULTS,
    RESPONSE_MODEL_NAME,
    SIMILARITY_THRESHOLD,
)

from vector_database_engine import (
    VectorDatabaseEngine,
)

# ============================================================
# PROJECT PATHS
# ============================================================
#
# app.py lives inside:
#
# capabilities/
#   heritage-intelligence-engine/
#     releases/
#       release-010-response-generation-engine/
#
# The project root is calculated relative to this file.
#
# No absolute paths are used so the application can run on:
#
# • macOS
# • Windows
# • Linux
# • Google Colab
# ============================================================

CURRENT_DIRECTORY = Path(__file__).resolve().parent

PROJECT_ROOT = CURRENT_DIRECTORY.parents[3]

FOUNDATION_DATASET_DIRECTORY = (
    PROJECT_ROOT / "foundation-dataset"
)

MARKDOWN_DIRECTORY = (
    FOUNDATION_DATASET_DIRECTORY / "knowledge-cards"
)

PDF_DIRECTORY = (
    FOUNDATION_DATASET_DIRECTORY / "pdfs"
)
# ============================================================
# STARTUP BANNER
# ============================================================

print("=" * 70)
print("Mzansi AI Hub")
print("Heritage Intelligence Engine")
print("Release 010B - Full RAG Integration")
print("=" * 70)
# ============================================================
# KNOWLEDGE ACQUISITION LAYER
#
# Python files:
# providers/markdown_provider.py
# providers/pdf_provider.py
# ============================================================
#
# Providers are responsible only for reading source documents.
#
# MarkdownProvider
#     Reads heritage knowledge cards.
#
# PDFProvider
#     Reads heritage PDF documents.
#
# Both providers return a common document structure so the rest
# of the application never needs to know the original file type.
# ============================================================

markdown_provider = MarkdownProvider(
    directory_path=MARKDOWN_DIRECTORY,
)

pdf_provider = PDFProvider(
    directory_path=PDF_DIRECTORY,
)
# ============================================================
# CHUNKING LAYER
#
# Python file:
# chunking_engine.py
# ============================================================
#
# The Chunking Engine divides large heritage documents into
# smaller semantic units.
#
# Smaller chunks improve semantic retrieval accuracy and reduce
# unnecessary context supplied to the language model.
# ============================================================

chunking_engine = ChunkingEngine(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)
# ============================================================
# SEMANTIC REPRESENTATION LAYER
#
# Python file:
# embedding_engine.py
# ============================================================
#
# SentenceTransformer converts text into semantic vectors.
#
# The Hugging Face model is created here and injected into the
# Embedding Engine.
#
# Architecture:
#
# Application
#      ↓
# Embedding Engine
#      ↓
# SentenceTransformer
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

embedding_engine = EmbeddingEngine(
    model=embedding_model,
)

print("Embedding model loaded successfully.")
# ============================================================
# SEMANTIC MEMORY LAYER
#
# Python file:
# vector_database_engine.py
# ============================================================
#
# The Vector Database Engine stores semantic embeddings inside
# a FAISS index.
#
# Startup
#
# Embedded Chunks
#        ↓
# Vector Database Engine
#        ↓
# FAISS Index
#
# Runtime
#
# Query Embedding
#        ↓
# Semantic Search
#        ↓
# Candidate Chunks
# ============================================================

vector_database_engine = VectorDatabaseEngine()
# ============================================================
# RETRIEVAL POLICY LAYER
#
# Python file:
# retrieval_policy_engine.py
# ============================================================
#
# Semantic search may retrieve several candidate chunks.
#
# The Retrieval Policy Engine decides which of those chunks
# are relevant enough to continue.
#
# Current policy:
#
# similarity >= SIMILARITY_THRESHOLD
#
# Future policies may include:
#
# • Metadata filtering
# • Duplicate removal
# • Trusted source weighting
# • Date filtering
# • Confidence thresholds
# ============================================================

retrieval_policy_engine = RetrievalPolicyEngine(
    similarity_threshold=SIMILARITY_THRESHOLD,
)
# ============================================================
# CONTEXT LAYER
#
# Python file:
# context_engine.py
# ============================================================
#
# The Context Engine converts approved heritage chunks into one
# structured context string.
#
# Input
#
# Approved Chunks
#
# Output
#
# LLM-ready Context
#
# This engine does not retrieve knowledge or generate answers.
# ============================================================

context_engine = ContextEngine()
# ============================================================
# RESPONSE GENERATION TECHNOLOGY
#
# External Technology:
# Hugging Face Transformers
# ============================================================
#
# The tokenizer converts our controlled prompt into model inputs.
#
# The language model generates the grounded response.
#
# Both objects are created here and injected into the
# Response Generation Engine.
#
# Architecture
#
# Application
#      ↓
# Response Generation Engine
#      ↓
# Hugging Face Transformers
# ============================================================

print("\nLoading response-generation tokenizer...")

response_tokenizer = AutoTokenizer.from_pretrained(
    RESPONSE_MODEL_NAME
)

print("Loading response-generation model...")

response_model = AutoModelForSeq2SeqLM.from_pretrained(
    RESPONSE_MODEL_NAME
)

print("Response-generation model loaded successfully.")
# ============================================================
# RESPONSE GENERATION LAYER
#
# Python file:
# response_generation_engine.py
# ============================================================
#
# Receives:
#
# • User Question
# • LLM-ready Context
#
# Produces:
#
# • Grounded Heritage Answer
#
# This engine knows nothing about PDFs, embeddings,
# retrieval, FAISS or Gradio.
# ============================================================

response_generation_engine = ResponseGenerationEngine(
    model=response_model,
    tokenizer=response_tokenizer,
    max_new_tokens=MAX_RESPONSE_TOKENS,
)
# ============================================================
# APPLICATION LAYER
#
# Python file:
# application_engine.py
# ============================================================
#
# This is the orchestration layer.
#
# It coordinates every engine without implementing
# their responsibilities.
# ============================================================

application_engine = ApplicationEngine(
    providers=[
        markdown_provider,
        pdf_provider,
    ],
    chunking_engine=chunking_engine,
    embedding_engine=embedding_engine,
    vector_database_engine=vector_database_engine,
    retrieval_policy_engine=retrieval_policy_engine,
    context_engine=context_engine,
    response_generation_engine=response_generation_engine,
    max_results=MAX_RESULTS,
)
# ============================================================
# STARTUP PREPARATION
# ============================================================

print("\nPreparing heritage knowledge base...")

indexed_chunk_count = application_engine.prepare()

print(
    f"Knowledge base ready "
    f"({indexed_chunk_count} chunk(s) indexed)."
)
# ============================================================
# PRESENTATION LAYER
#
# Technology:
# Gradio
# ============================================================

def ask_heritage_question(query: str):
    """
    Process a heritage question through the complete AI pipeline.
    """

    result = application_engine.ask(query)

    return (
        result["answer"],
        result["message"],
    )


with gr.Blocks(
    title="Mzansi AI Hub | Heritage Intelligence Engine",
) as demo:

    gr.Markdown(
        """
# 🇿🇦 Mzansi AI Hub

## Heritage Intelligence Engine

Ask questions about South African heritage.

The system retrieves heritage knowledge and generates
grounded answers using AI.
"""
    )

    question = gr.Textbox(
        label="Heritage Question",
        placeholder="Example: Why is Robben Island historically significant?",
        lines=3,
    )

    answer = gr.Textbox(
        label="Grounded Heritage Answer",
        lines=10,
    )

    status = gr.Textbox(
        label="System Status",
    )

    ask_button = gr.Button(
        "Ask",
        variant="primary",
    )

    ask_button.click(
        fn=ask_heritage_question,
        inputs=question,
        outputs=[
            answer,
            status,
        ],
    )

    question.submit(
        fn=ask_heritage_question,
        inputs=question,
        outputs=[
            answer,
            status,
        ],
    )