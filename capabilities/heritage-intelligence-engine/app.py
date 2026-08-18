"""
Mzansi AI Hub
Heritage Intelligence Engine

Top-Level Runtime Application

This file is the end-to-end runtime blueprint.

It connects:

External models
    ↓
Capability bootstraps
    ↓
HeritageApplication
    ↓
Knowledge preparation
    ↓
Gradio presentation layer
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
# External Technology Configuration
# ============================================================

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

GENERATION_MODEL_NAME = (
    "Qwen/Qwen2.5-1.5B-Instruct"
)


# ============================================================
# Model Loading
# ============================================================
#
# External technologies are loaded here.
#
# They are then passed into our own architectural contracts.
#
# Sentence Transformers
#       ↓
# EmbeddingEngine
#
# Qwen + Hugging Face
#       ↓
# HuggingFaceGenerationProvider
#
# The external libraries do not define our architecture.
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

print("Embedding model ready.")


print("Loading generation tokenizer...")

generation_tokenizer = AutoTokenizer.from_pretrained(
    GENERATION_MODEL_NAME
)

print("Loading generation model...")

generation_model = AutoModelForCausalLM.from_pretrained(
    GENERATION_MODEL_NAME,
    torch_dtype="auto",
    device_map="auto",
)

print("Generation model ready.")


# ============================================================
# Application Assembly
# ============================================================
#
# applications/bootstrap.py assembles:
#
# Semantic Retrieval
#       ↓
# Evidence Retrieval
#
# Response Generation
#       ↓
# Generation Provider
#
# All capabilities are then exposed through:
#
# HeritageApplication
#
# Public application API:
#
# heritage_application.prepare()
# heritage_application.ask(question)
# ============================================================

print("Assembling Heritage Intelligence application...")

heritage_application = create_heritage_application(
    embedding_model=embedding_model,
    generation_model=generation_model,
    generation_tokenizer=generation_tokenizer,
)

print("Heritage Intelligence application assembled.")


# ============================================================
# Knowledge Preparation
# ============================================================
#
# Startup preparation flow:
#
# datasets/
#     ↓
# Providers
#     ↓
# Standard documents
#     ↓
# Chunking Engine
#     ↓
# Page-aware chunks
#     ↓
# Embedding Engine
#     ↓
# Embedded chunks
#     ↓
# Vector Database Engine
#     ↓
# FAISS index
#
# If new PDFs or knowledge cards are added to datasets/,
# restarting the application and running prepare() again
# rebuilds the searchable intelligence with the new data.
# ============================================================

print("Preparing heritage knowledge...")

prepared_count = heritage_application.prepare()

print(
    f"Heritage knowledge ready. "
    f"Prepared {prepared_count} searchable chunks."
)


# ============================================================
# Gradio Presentation Adapter
# ============================================================
#
# Gradio has ONE job:
#
# User question
#       ↓
# heritage_application.ask()
#       ↓
# answer + source summaries
#       ↓
# display
#
# Gradio does NOT:
#
# - read PDFs
# - chunk documents
# - generate embeddings
# - search FAISS
# - retrieve evidence directly
# - call Qwen directly
#
# All intelligence remains behind HeritageApplication.
# ============================================================

def ask_heritage(
    question: str,
    progress=gr.Progress(),
):
    """
    Send a heritage question through the complete
    Heritage Intelligence Engine.

    Returns
    -------
    tuple
        answer_markdown
        sources_markdown
    """

    if not question or not question.strip():
        return (
            "Please enter a heritage question.",
            "",
        )

    try:

        progress(
            0.10,
            desc="Receiving heritage question...",
        )

        progress(
            0.30,
            desc="Retrieving relevant heritage evidence...",
        )

        response = heritage_application.ask(
            question
        )

        progress(
            0.75,
            desc="Generating grounded response...",
        )

        answer = response.get(
            "answer",
            "",
        )

        sources = response.get(
            "sources",
            [],
        )

        # -----------------------------------------------------
        # Format source provenance for the UI.
        # -----------------------------------------------------

        source_lines = []

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

            source_lines.append(
                f"### {index}. {title}"
            )

            if filename:
                source_lines.append(
                    f"**File:** `{filename}`"
                )

            if page_number is not None:
                source_lines.append(
                    f"**Page:** `{page_number}`"
                )

            source_lines.append(
                "**Semantic similarity:** "
                f"`{similarity:.4f}`"
            )

            source_lines.append("")

        sources_markdown = "\n".join(
            source_lines
        )

        progress(
            1.0,
            desc="Heritage response ready.",
        )

        return (
            answer,
            sources_markdown,
        )

    except Exception as error:

        return (
            (
                "## Application error\n\n"
                f"```text\n"
                f"{type(error).__name__}: {error}\n"
                f"```"
            ),
            "",
        )


# ============================================================
# Gradio Interface
# ============================================================

with gr.Blocks(
    title="Mzansi AI Hub — Heritage Intelligence",
) as demo:

    gr.Markdown(
        """
# Mzansi AI Hub
## Heritage Intelligence Engine

Ask questions grounded in the configured South African
heritage knowledge base.

The application retrieves relevant evidence first,
then generates an answer grounded in that evidence.
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
        "Ask Heritage Intelligence"
    )

    gr.Markdown("## Answer")

    answer_output = gr.Markdown()

    gr.Markdown("## Sources")

    sources_output = gr.Markdown()

    gr.Examples(
        examples=[
            ["Tell me about Mapungubwe"],
            ["Who was Charlotte Maxeke?"],
            ["What is the significance of Robben Island?"],
            ["Tell me about Ndebele art"],
            ["What is the Cradle of Humankind?"],
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
# queue() enables queued Gradio execution and allows the
# visible gr.Progress indicator to update during requests.
# ============================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch()