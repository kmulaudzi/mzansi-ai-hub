"""
Mzansi AI Hub
Heritage Intelligence Engine

Top-Level Runtime Application

This file is the end-to-end runtime blueprint.

It connects:

External AI Technologies
        ↓
Heritage Intelligence Architecture
        ↓
Persistent Semantic Intelligence
        ↓
HeritageApplication
        ↓
Gradio
"""

import gradio as gr
import torch

from sentence_transformers import SentenceTransformer
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
)

from applications.bootstrap import (
    create_application as create_heritage_application,
)


# ============================================================
# Model Configuration
# ============================================================

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

GENERATION_MODEL_NAME = (
    "Qwen/Qwen2.5-1.5B-Instruct"
)


# ============================================================
# External Technology Loading
# ============================================================
#
# External technologies remain behind our own contracts:
#
# Sentence Transformers
#       ↓
# EmbeddingEngine
#
# Qwen + Hugging Face
#       ↓
# HuggingFaceGenerationProvider
#
# FAISS
#       ↓
# VectorDatabaseEngine
#
# Gradio
#       ↓
# Presentation Layer
#
# ============================================================


def load_embedding_model():
    """
    Load the embedding model used by Semantic Retrieval.
    """

    print(
        f"Loading embedding model: "
        f"{EMBEDDING_MODEL_NAME}"
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    print("Embedding model ready.")

    return model


def load_generation_model():
    """
    Load the generation model and tokenizer.

    device_map='auto' places Qwen on GPU when available.
    """

    print(
        f"Loading generation model: "
        f"{GENERATION_MODEL_NAME}"
    )

    tokenizer = AutoTokenizer.from_pretrained(
        GENERATION_MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        GENERATION_MODEL_NAME,
        torch_dtype="auto",
        device_map="auto",
    )

    print("Generation model ready.")

    print(
        "CUDA available:",
        torch.cuda.is_available(),
    )

    print(
        "Generation model device:",
        model.device,
    )

    return model, tokenizer


# ============================================================
# Load Models
# ============================================================

embedding_model = load_embedding_model()

(
    generation_model,
    generation_tokenizer,
) = load_generation_model()


# ============================================================
# Assemble Heritage Application
# ============================================================
#
# applications/bootstrap.py assembles:
#
# Semantic Retrieval
#       ↓
# Evidence Retrieval
#
# Response Generation
#
# into:
#
# HeritageApplication
#
# Public API:
#
# heritage_application.prepare()
# heritage_application.ask(question)
#
# ============================================================

print(
    "Assembling Heritage Intelligence application..."
)

heritage_application = (
    create_heritage_application(
        embedding_model=embedding_model,
        generation_model=generation_model,
        generation_tokenizer=(
            generation_tokenizer
        ),
    )
)

print(
    "Heritage Intelligence application assembled."
)


# ============================================================
# Prepare Persistent Semantic Intelligence
# ============================================================
#
# prepare() now has two paths:
#
# FAST PATH
# ----------
# Existing persisted intelligence
# +
# unchanged dataset fingerprint
#       ↓
# load FAISS index + chunk metadata
#       ↓
# ready almost immediately
#
#
# REBUILD PATH
# ------------
# New/changed PDF or knowledge card
#       ↓
# Providers
#       ↓
# Page-aware documents
#       ↓
# ChunkingEngine
#       ↓
# EmbeddingEngine
#       ↓
# VectorDatabaseEngine
#       ↓
# persist new intelligence
#
# ============================================================

print(
    "Preparing heritage intelligence..."
)

prepared_count = (
    heritage_application.prepare()
)

print(
    f"Heritage intelligence ready: "
    f"{prepared_count} searchable chunks."
)


# ============================================================
# Source Formatting
# ============================================================


def format_sources(
    sources,
):
    """
    Convert source summaries into Markdown.
    """

    if not sources:
        return (
            "No supporting sources were returned."
        )

    output = []

    for index, source in enumerate(
        sources,
        start=1,
    ):
        title = source.get(
            "title",
            "Unknown source",
        )

        filename = source.get(
            "filename",
            "",
        )

        page_number = source.get(
            "page_number",
        )

        similarity = source.get(
            "similarity",
            0.0,
        )

        output.append(
            f"### {index}. {title}"
        )

        if filename:
            output.append(
                f"**File:** `{filename}`"
            )

        if page_number is not None:
            output.append(
                f"**Page:** `{page_number}`"
            )

        output.append(
            "**Semantic similarity:** "
            f"`{similarity:.4f}`"
        )

        output.append("")

    return "\n".join(output)


# ============================================================
# Gradio Adapter
# ============================================================
#
# Gradio remains thin.
#
# It knows only:
#
# question
#    ↓
# heritage_application.ask()
#    ↓
# answer + sources
#
# ============================================================


def ask_heritage(
    question: str,
    progress=gr.Progress(),
):
    """
    Send a question through the complete
    Heritage Intelligence Engine.
    """

    if not question or not question.strip():
        return (
            "Please enter a heritage question.",
            "",
        )

    try:

        progress(
            0.10,
            desc="Receiving question...",
        )

        progress(
            0.30,
            desc=(
                "Retrieving evidence and "
                "generating grounded response..."
            ),
        )

        response = (
            heritage_application.ask(
                question
            )
        )

        progress(
            0.90,
            desc="Formatting sources...",
        )

        answer = response.get(
            "answer",
            "",
        )

        sources_markdown = (
            format_sources(
                response.get(
                    "sources",
                    [],
                )
            )
        )

        progress(
            1.0,
            desc="Response ready.",
        )

        return (
            answer,
            sources_markdown,
        )

    except Exception as error:

        return (
            (
                "## Application Error\n\n"
                "```text\n"
                f"{type(error).__name__}: "
                f"{error}\n"
                "```"
            ),
            "",
        )


# ============================================================
# Gradio Interface
# ============================================================

with gr.Blocks(
    title=(
        "Mzansi AI Hub — "
        "Heritage Intelligence Engine"
    ),
) as demo:

    gr.Markdown(
        """
# Mzansi AI Hub

## Heritage Intelligence Engine

Ask questions grounded in the configured
South African heritage knowledge base.

The system retrieves supporting evidence first,
then generates a grounded answer.
"""
    )

    question_input = gr.Textbox(
        label="Ask a Heritage Question",
        placeholder=(
            "Example: Tell me about Mapungubwe"
        ),
        lines=2,
    )

    ask_button = gr.Button(
        "Ask Heritage Intelligence",
        variant="primary",
    )

    gr.Markdown(
        "## Answer"
    )

    answer_output = gr.Markdown()

    gr.Markdown(
        "## Supporting Sources"
    )

    sources_output = gr.Markdown()

    gr.Examples(
        examples=[
            [
                "Tell me about Mapungubwe"
            ],
            [
                "Who was Charlotte Maxeke?"
            ],
            [
                "What is the significance "
                "of Robben Island?"
            ],
            [
                "Tell me about Ndebele art"
            ],
            [
                "What is the Cradle of Humankind?"
            ],
        ],
        inputs=question_input,
    )

    ask_button.click(
        fn=ask_heritage,
        inputs=question_input,
        outputs=[
            answer_output,
            sources_output,
        ],
    )

    question_input.submit(
        fn=ask_heritage,
        inputs=question_input,
        outputs=[
            answer_output,
            sources_output,
        ],
    )


# ============================================================
# Runtime Launch
# ============================================================
#
# queue()
# enables queued execution and Gradio progress updates.
#
# share=True
# is useful in Colab for a temporary public demo URL.
#
# ============================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch(
        share=True,
    )