"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine

Runtime Blueprint
-----------------
This file creates and connects every component required by the
Heritage Intelligence Engine.

The application has two separate pipelines:

1. Startup pipeline
   Loads, chunks, embeds and indexes heritage documents once.

2. Runtime pipeline
   Receives a question, retrieves relevant knowledge, builds context
   and generates a grounded answer.
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
from response_generation_engine import ResponseGenerationEngine
from retrieval_policy_engine import RetrievalPolicyEngine
from settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    MAX_RESULTS,
    RESPONSE_MODEL_NAME,
    SIMILARITY_THRESHOLD,
)
from vector_database_engine import VectorDatabaseEngine


# =============================================================
# PROJECT PATHS
# =============================================================
#
# app.py lives inside:
#
# capabilities/
#   heritage-intelligence-engine/
#     releases/
#       release-010-response-generation-engine/
#
# The project root is calculated relative to this file instead
# of depending on the terminal's current working directory.
# =============================================================

CURRENT_DIRECTORY = Path(__file__).resolve().parent

PROJECT_ROOT = CURRENT_DIRECTORY.parents[3]

FOUNDATION_DATASET_DIRECTORY = (
    PROJECT_ROOT
    / "foundation-dataset"
)

MARKDOWN_DIRECTORY = (
    FOUNDATION_DATASET_DIRECTORY
    / "knowledge-cards"
)

PDF_DIRECTORY = (
    FOUNDATION_DATASET_DIRECTORY
    / "pdfs"
)


# =============================================================
# STARTUP BANNER
# =============================================================

print("=" * 70)
print("Mzansi AI Hub")
print("Heritage Intelligence Engine")
print("Release 010 - Response Generation Engine")
print("=" * 70)


# =============================================================
# KNOWLEDGE ACQUISITION LAYER
#
# Python files:
# providers/markdown_provider.py
# providers/pdf_provider.py
# =============================================================
#
# Providers are responsible only for reading source documents.
#
# MarkdownProvider
#     Reads Markdown heritage knowledge cards.
#
# PDFProvider
#     Reads heritage PDF documents.
#
# Providers return a common document structure so that the rest
# of the application does not need to know which file format was
# originally used.
# =============================================================

markdown_provider = MarkdownProvider(
    directory_path=MARKDOWN_DIRECTORY,
)

pdf_provider = PDFProvider(
    directory_path=PDF_DIRECTORY,
)


# =============================================================
# KNOWLEDGE SEGMENTATION LAYER
#
# Python file:
# chunking_engine.py
# =============================================================
#
# The Chunking Engine divides large documents into smaller,
# searchable knowledge units.
#
# It preserves document metadata so that each chunk can still be
# traced back to its title, source and original document.
# =============================================================

chunking_engine = ChunkingEngine(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


# =============================================================
# SEMANTIC REPRESENTATION LAYER
#
# Python file:
# embedding_engine.py
# =============================================================
#
# SentenceTransformer is an external Hugging Face technology.
#
# It is created here and injected into EmbeddingEngine.
#
# This means the rest of the application communicates with our
# own EmbeddingEngine contract rather than communicating directly
# with SentenceTransformer.
#
# Architecture:
#
# Application
#     ↓
# EmbeddingEngine
#     ↓
# SentenceTransformer
# =============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

embedding_engine = EmbeddingEngine(
    model=embedding_model,
)

print("Embedding model loaded successfully.")


# =============================================================
# SEMANTIC MEMORY LAYER
#
# Python file:
# vector_database_engine.py
# =============================================================
#
# The Vector Database Engine stores embedded heritage chunks in
# a FAISS index.
#
# Startup:
#
# Embedded chunks
#     ↓
# VectorDatabaseEngine.build_index()
#     ↓
# FAISS vector index
#
# Runtime:
#
# Query embedding
#     ↓
# VectorDatabaseEngine.search()
#     ↓
# Candidate heritage chunks
#
# FAISS remains hidden behind our own architecture.
# =============================================================

vector_database_engine = VectorDatabaseEngine()


# =============================================================
# KNOWLEDGE JUDGEMENT LAYER
#
# Python file:
# retrieval_policy_engine.py
# =============================================================
#
# The Vector Database Engine finds semantically close chunks.
#
# The Retrieval Policy Engine then decides which candidates are
# relevant enough to continue through the pipeline.
#
# Current policy:
#
# similarity >= SIMILARITY_THRESHOLD
#
# Future policies may include:
#
# - trusted-source weighting
# - metadata filtering
# - date filtering
# - duplicate removal
# - content safety rules
# - source authority rules
# =============================================================

retrieval_policy_engine = RetrievalPolicyEngine(
    similarity_threshold=SIMILARITY_THRESHOLD,
)


# =============================================================
# KNOWLEDGE ORGANISATION LAYER
#
# Python file:
# context_engine.py
# =============================================================
#
# The Context Engine converts approved heritage chunks into one
# structured context string.
#
# Input:
#
# List[Dict]
#
# Output:
#
# One LLM-ready string
#
# It does not retrieve knowledge and it does not generate answers.
# =============================================================

context_engine = ContextEngine()


# =============================================================
# RESPONSE-GENERATION TECHNOLOGY
#
# External implementation:
# Hugging Face Transformers
# =============================================================
#
# The tokenizer converts the controlled prompt into model inputs.
#
# The model generates a natural-language response.
#
# These objects are created outside ResponseGenerationEngine and
# injected into it. This preserves dependency injection and keeps
# Hugging Face behind our architectural contract.
# =============================================================

print("\nLoading response-generation tokenizer...")

response_tokenizer = AutoTokenizer.from_pretrained(
    RESPONSE_MODEL_NAME
)

print("Loading response-generation model...")

response_model = AutoModelForSeq2SeqLM.from_pretrained(
    RESPONSE_MODEL_NAME
)

print("Response-generation model loaded successfully.")


# =============================================================
# RESPONSE GENERATION LAYER
#
# Python file:
# response_generation_engine.py
# =============================================================
#
# The Response Generation Engine receives:
#
# - the user's question
# - the context built from approved heritage knowledge
#
# It then:
#
# 1. Builds a controlled prompt.
# 2. Tokenizes the prompt.
# 3. Calls the language model.
# 4. Decodes the generated output.
# 5. Returns the grounded answer.
#
# It does not know about PDFs, Markdown, chunks, FAISS or Gradio.
# =============================================================

response_generation_engine = ResponseGenerationEngine(
    model=response_model,
    tokenizer=response_tokenizer,
)


# =============================================================
# APPLICATION COORDINATION LAYER
#
# Python file:
# application_engine.py
# =============================================================
#
# ApplicationEngine coordinates the complete user-facing flow.
#
# It receives all dependencies rather than constructing them.
#
# This is the composition root of the application: the location
# where independently designed components are connected.
# =============================================================

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


# =============================================================
# STARTUP PIPELINE
# =============================================================
#
# This work happens once when the application starts.
#
# MarkdownProvider / PDFProvider
# providers/*.py
#         ↓
# Documents
#         ↓
# ChunkingEngine
# chunking_engine.py
#         ↓
# Chunks
#         ↓
# EmbeddingEngine
# embedding_engine.py
#         ↓
# Embedded chunks
#         ↓
# VectorDatabaseEngine
# vector_database_engine.py
#         ↓
# FAISS vector index
#
# Expensive document embeddings are therefore not regenerated
# for every user question.
# =============================================================

print("\nPreparing heritage knowledge...")

indexed_chunk_count = application_engine.prepare()

print(
    f"Heritage knowledge prepared successfully. "
    f"{indexed_chunk_count} chunk(s) indexed."
)


# =============================================================
# GRADIO CALLBACK
# =============================================================
#
# This function connects the presentation layer to our
# ApplicationEngine.
#
# Runtime pipeline:
#
# User question
#     ↓
# ApplicationEngine.ask()
# application_engine.py
#     ↓
# RetrievalEngine.retrieve()
# retrieval_engine.py
#     ↓
# EmbeddingEngine.embed_text()
# embedding_engine.py
#     ↓
# Query embedding
#     ↓
# VectorDatabaseEngine.search()
# vector_database_engine.py
#     ↓
# Candidate chunks
#     ↓
# RetrievalPolicyEngine.apply()
# retrieval_policy_engine.py
#     ↓
# Approved chunks
#     ↓
# ContextEngine.build_context()
# context_engine.py
#     ↓
# LLM-ready context
#     ↓
# ResponseGenerationEngine.generate_response()
# response_generation_engine.py
#     ↓
# Grounded heritage answer
#     ↓
# Gradio output
# =============================================================

def ask_heritage_question(
    query: str,
    progress=gr.Progress(),
):
    """
    Process a heritage question through the complete RAG pipeline.

    Returns
    -------
    tuple
        Generated answer, status message, source text and context.
    """

    progress(
        0.05,
        desc="Validating your question...",
    )

    clean_query = (query or "").strip()

    if not clean_query:
        return (
            "",
            "Please enter a heritage question.",
            "",
            "",
        )

    progress(
        0.20,
        desc="Searching heritage knowledge...",
    )

    result = application_engine.ask(
        query=clean_query
    )

    progress(
        0.75,
        desc="Preparing grounded response...",
    )

    answer = result.get(
        "answer",
        "",
    )

    message = result.get(
        "message",
        "",
    )

    context = result.get(
        "context",
        "",
    )

    approved_chunks = result.get(
        "results",
        [],
    )

    source_sections = []

    for position, chunk in enumerate(
        approved_chunks,
        start=1,
    ):
        title = str(
            chunk.get(
                "title",
                "Unknown source",
            )
        ).strip()

        source = str(
            chunk.get(
                "source",
                "Unknown file",
            )
        ).strip()

        similarity = chunk.get(
            "similarity"
        )

        source_lines = [
            f"### {position}. {title}",
            f"**Source:** {source}",
        ]

        if similarity is not None:
            source_lines.append(
                f"**Similarity:** {float(similarity):.4f}"
            )

        source_sections.append(
            "\n\n".join(source_lines)
        )

    formatted_sources = (
        "\n\n---\n\n".join(source_sections)
        if source_sections
        else "No approved sources were returned."
    )

    progress(
        1.0,
        desc="Answer ready.",
    )

    return (
        answer,
        message,
        formatted_sources,
        context,
    )


# =============================================================
# PRESENTATION LAYER
#
# Technology:
# Gradio
# =============================================================
#
# Gradio is only responsible for:
#
# - collecting the user's question
# - displaying the generated answer
# - displaying development information
#
# It does not contain retrieval or AI logic.
# =============================================================

with gr.Blocks(
    title="Mzansi AI Hub | Heritage Intelligence Engine"
) as demo:

    gr.Markdown(
        """
# Mzansi AI Hub

## Heritage Intelligence Engine

Ask a question about South African heritage.

The application retrieves relevant knowledge from the heritage
document collection and generates a grounded answer using only
the approved context.
"""
    )

    with gr.Row():

        with gr.Column(scale=2):

            question_input = gr.Textbox(
                label="Heritage Question",
                placeholder=(
                    "Example: Why is Robben Island "
                    "historically significant?"
                ),
                lines=3,
            )

            ask_button = gr.Button(
                "Ask the Heritage Intelligence Engine",
                variant="primary",
            )

            clear_button = gr.ClearButton(
                value="Clear",
            )

        with gr.Column(scale=3):

            answer_output = gr.Textbox(
                label="Grounded Heritage Answer",
                lines=10,
                interactive=False,
            )

            status_output = gr.Textbox(
                label="System Status",
                lines=2,
                interactive=False,
            )

    with gr.Accordion(
        "Approved Heritage Sources",
        open=False,
    ):
        sources_output = gr.Markdown()

    with gr.Accordion(
        "Development View: LLM-Ready Context",
        open=False,
    ):
        context_output = gr.Textbox(
            label="Context sent to the response model",
            lines=16,
            interactive=False,
        )

    ask_button.click(
        fn=ask_heritage_question,
        inputs=[
            question_input,
        ],
        outputs=[
            answer_output,
            status_output,
            sources_output,
            context_output,
        ],
    )

    question_input.submit(
        fn=ask_heritage_question,
        inputs=[
            question_input,
        ],
        outputs=[
            answer_output,
            status_output,
            sources_output,
            context_output,
        ],
    )

    clear_button.add(
        components=[
            question_input,
            answer_output,
            status_output,
            sources_output,
            context_output,
        ]
    )


# =============================================================
# APPLICATION LAUNCH
# =============================================================

if __name__ == "__main__":
    demo.launch(
        share=True,
        debug=True,
    )