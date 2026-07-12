"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 005 - Embedding Engine

Gradio Interface
"""

from typing import Any

import gradio as gr

from application_engine import ApplicationEngine
from chunking_engine import ChunkingEngine
from embedding_engine import EmbeddingEngine
from providers.markdown_provider import MarkdownProvider
from providers.pdf_provider import PDFProvider
from settings import (
    APPLICATION_DESCRIPTION,
    APPLICATION_NAME,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATASET_PATH,
    MAX_RESULTS,
    PDF_DATASET_PATH,
    RESULTS_LABEL,
    SEARCH_LABEL,
    SEARCH_PLACEHOLDER,
    WINDOW_TITLE,
)


def create_demo(embedding_model: Any) -> gr.Interface:
    """
    Build the Gradio application using an injected embedding model.
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

    application_engine = ApplicationEngine(
        providers=[
            markdown_provider,
            pdf_provider,
        ],
        chunking_engine=chunking_engine,
        embedding_engine=embedding_engine,
        max_results=MAX_RESULTS,
    )

    def format_search_results(query: str) -> str:
        response = application_engine.search(query)

        if response["result_count"] == 0:
            return response["message"]

        output = [
            f"## {response['message']}",
            "",
        ]

        for index, result in enumerate(
            response["results"],
            start=1,
        ):
            output.extend(
                [
                    f"### {index}. {result['title']}",
                    "",
                    f"**Relevance score:** {result['score']}",
                    "",
                    f"**Source type:** `{result['source_type']}`",
                    "",
                    f"**Source file:** `{result['filename']}`",
                    "",
                    f"**Chunk ID:** `{result['chunk_id']}`",
                    "",
                    f"**Chunk index:** `{result['chunk_index']}`",
                    "",
                    (
                        "**Embedding dimension:** "
                        f"`{result['embedding_dimension']}`"
                    ),
                    "",
                    f"**Parent document:** `{result['parent_document']}`",
                    "",
                    result["content"],
                    "",
                    "---",
                    "",
                ]
            )

        return "\n".join(output)

    return gr.Interface(
        fn=format_search_results,
        inputs=gr.Textbox(
            label=SEARCH_LABEL,
            placeholder=SEARCH_PLACEHOLDER,
            lines=1,
        ),
        outputs=gr.Markdown(
            label=RESULTS_LABEL,
        ),
        title=f"{APPLICATION_NAME} — {WINDOW_TITLE}",
        description=APPLICATION_DESCRIPTION,
        examples=[
            ["Mandela"],
            ["women leaders"],
            ["living heritage"],
            ["funding"],
            ["museum"],
        ],
    )