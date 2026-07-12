"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 003 - Document Intelligence

Gradio Interface
"""

import gradio as gr

from application_engine import ApplicationEngine
from providers.markdown_provider import MarkdownProvider
from providers.pdf_provider import PDFProvider
from settings import (
    APPLICATION_DESCRIPTION,
    APPLICATION_NAME,
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
# Application Engine
# -------------------------------------------------------------------

application_engine = ApplicationEngine(
    providers=[
        markdown_provider,
        pdf_provider,
    ],
    max_results=MAX_RESULTS,
)


# -------------------------------------------------------------------
# Interface Adapter
# -------------------------------------------------------------------

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
        ["women leaders"],
        ["heritage art"],
        ["kingdom"],
    ],
)


if __name__ == "__main__":
    demo.launch()