"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 005 - Embedding Engine

Gradio Interface and Runtime Blueprint
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
    Build the complete Release 005 application.

    Runtime flow
    ------------
    1. Colab loads the Hugging Face embedding model.
    2. Colab passes that model into create_demo().
    3. This function creates the Providers.
    4. It creates the Chunking Engine.
    5. It connects the Hugging Face model to our Embedding Engine.
    6. It creates the Application Engine.
    7. It creates and returns the Gradio interface.
    """

    # -------------------------------------------------------------
    # Provider Layer
    # -------------------------------------------------------------
    # Providers read different source formats and return the same
    # standard document structure.
    # -------------------------------------------------------------

    markdown_provider = MarkdownProvider(
        source_path=str(DATASET_PATH)
    )

    pdf_provider = PDFProvider(
        source_path=str(PDF_DATASET_PATH)
    )

    # -------------------------------------------------------------
    # Chunking Layer
    # -------------------------------------------------------------
    # The Chunking Engine divides large documents into smaller,
    # searchable pieces while preserving source metadata.
    # -------------------------------------------------------------

    chunking_engine = ChunkingEngine(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # -------------------------------------------------------------
    # Embedding Layer
    # -------------------------------------------------------------
    # embedding_model is the real Hugging Face model created in Colab.
    #
    # EmbeddingEngine is our architectural wrapper around that model.
    #
    # This line is where the external model becomes connected to our
    # Heritage Intelligence Engine.
    # -------------------------------------------------------------

    embedding_engine = EmbeddingEngine(
        model=embedding_model
    )

    # -------------------------------------------------------------
    # Application Layer
    # -------------------------------------------------------------
    # The Application Engine connects the Providers, Chunking Engine,
    # Embedding Engine, Retrieval Engine, Search Engine and Ranking
    # Engine into one application workflow.
    # -------------------------------------------------------------

    application_engine = ApplicationEngine(
        providers=[
            markdown_provider,
            pdf_provider,
        ],
        chunking_engine=chunking_engine,
        embedding_engine=embedding_engine,
        max_results=MAX_RESULTS,
    )

    # -------------------------------------------------------------
    # Gradio Adapter
    # -------------------------------------------------------------
    # Gradio receives a query and passes it to the Application Engine.
    #
    # Gradio does not load documents, chunk text, create embeddings,
    # search, or rank. It only sends input and displays output.
    # -------------------------------------------------------------

    def format_search_results(
        query: str,
        progress=gr.Progress(),
    ) -> str:
        """
        Process one user search and format the results as Markdown.
        """

        if not query or not query.strip():
            return "Please enter a search query."

        try:
            progress(
                0.1,
                desc="Starting the Heritage Intelligence Engine...",
            )

            progress(
                0.25,
                desc="Loading Markdown and PDF documents...",
            )

            progress(
                0.45,
                desc="Creating document chunks...",
            )

            progress(
                0.65,
                desc="Generating embeddings...",
            )

            progress(
                0.85,
                desc="Searching and ranking heritage knowledge...",
            )

            response = application_engine.search(query)

            progress(
                1.0,
                desc="Results ready.",
            )

        except Exception as error:
            return (
                "## Application error\n\n"
                f"```text\n{type(error).__name__}: {error}\n```"
            )

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
                    f"**Relevance score:** `{result['score']}`",
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
                    (
                        "**Parent document:** "
                        f"`{result['parent_document']}`"
                    ),
                    "",
                    result["content"],
                    "",
                    "---",
                    "",
                ]
            )

        return "\n".join(output)

    # -------------------------------------------------------------
    # Gradio Interface
    # -------------------------------------------------------------

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