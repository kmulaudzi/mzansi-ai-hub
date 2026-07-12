"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 004 - Document Chunking Engine

Gradio Interface
"""

import gradio as gr

from application_engine import ApplicationEngine
from chunking_engine import ChunkingEngine
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


# -------------------------------------------------------------------
# Providers
# -------------------------------------------------------------------

markdown_provider = MarkdownProvider(
    source_path=str(DATASET_PATH)
)

pdf_provider = PDFProvider(
    source_path=str(PDF_DATASET_PATH)
)


# -------------------------------------------------------------------
# Chunking Engine
# -------------------------------------------------------------------

chunking_engine = ChunkingEngine(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


# -------------------------------------------------------------------
# Application Engine
# -------------------------------------------------------------------

application_engine = ApplicationEngine(
    providers=[
        markdown_provider,
        pdf_provider,
    ],
    chunking_engine=chunking_engine,
    max_results=MAX_RESULTS,
)


# -------------------------------------------------------------------
# Interface Adapter
# -------------------------------------------------------------------

def format_search_results(query: str) -> str:
    """
    Convert the Application Engine response into Markdown
    for display in the Gradio interface.
    """

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
                f"**Parent document:** `{result['parent_document']}`",
                "",
                result["content"],
                "",
                "---",
                "",
            ]
        )

    return "\n".join(output)


# -------------------------------------------------------------------
# Gradio Interface
# -------------------------------------------------------------------

demo = gr.Interface(
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
        ["heritage art"],
        ["living heritage"],
        ["funding"],
        ["museum"],
    ],
)


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    demo.launch()