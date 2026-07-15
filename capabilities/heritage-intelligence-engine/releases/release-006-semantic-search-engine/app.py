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
    3. This function creates the document Providers.
    4. It creates the Chunking Engine.
    5. It connects the Hugging Face model to our Embedding Engine.
    6. It creates the Application Engine.
    7. It prepares and caches the heritage knowledge once.
    8. It creates and returns the Gradio interface.
    """

    # -------------------------------------------------------------
    # Provider Layer
    # -------------------------------------------------------------
    # Providers read different source formats and convert them into
    # the platform's standard document structure.
    #
    # MarkdownProvider reads the Knowledge Cards.
    # PDFProvider reads the heritage PDF collection.
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
    # embedding_model is the real Hugging Face model loaded in Colab.
    #
    # EmbeddingEngine is our architectural wrapper around that model.
    #
    # This is where the external Hugging Face model becomes connected
    # to the Heritage Intelligence Engine.
    # -------------------------------------------------------------

    embedding_engine = EmbeddingEngine(
        model=embedding_model
    )

    # -------------------------------------------------------------
    # Application Layer
    # -------------------------------------------------------------
    # The Application Engine coordinates the complete workflow.
    #
    # It connects:
    #   - Providers
    #   - Chunking Engine
    #   - Embedding Engine
    #   - Retrieval Engine
    #   - Search Engine
    #   - Ranking Engine
    #
    # Gradio only talks to the Application Engine.
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
    # Prepare and Cache Heritage Knowledge
    # -------------------------------------------------------------
    # This runs once when create_demo() is called.
    #
    # It:
    #   1. Loads Markdown and PDF documents.
    #   2. Creates document chunks.
    #   3. Generates embeddings for those chunks.
    #   4. Stores the embedded chunks in memory.
    #
    # Every user search then reuses the cached chunks.
    # -------------------------------------------------------------

    print("Preparing heritage knowledge...")

    cached_chunk_count = application_engine.prepare()

    print(
        f"Heritage knowledge ready. "
        f"Cached {cached_chunk_count} embedded chunks."
    )

    # -------------------------------------------------------------
    # Gradio Adapter
    # -------------------------------------------------------------
    # Gradio receives the user's query and passes it to the
    # Application Engine.
    #
    # Gradio does not:
    #   - Load documents
    #   - Create chunks
    #   - Generate embeddings
    #   - Search documents
    #   - Rank results
    #
    # It only sends input and displays output.
    # -------------------------------------------------------------

    def format_search_results(
        query: str,
        progress=gr.Progress(),
    ) -> str:
        """
        Search the prepared in-memory heritage knowledge.

        Search-time flow
        ----------------
        1. Receive the user's query.
        2. Search the cached embedded chunks.
        3. Rank matching chunks.
        4. Format the results for Gradio.
        """

        if not query or not query.strip():
            return "Please enter a search query."

        try:
            progress(
                0.2,
                desc="Receiving search query...",
            )

            progress(
                0.6,
                desc="Searching cached heritage chunks...",
            )

            response = application_engine.search(query)

            progress(
                0.85,
                desc="Formatting ranked results...",
            )

        except Exception as error:
            return (
                "## Application error\n\n"
                f"```text\n{type(error).__name__}: {error}\n```"
            )

        if response["result_count"] == 0:
            progress(
                1.0,
                desc="Search complete.",
            )

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

        progress(
            1.0,
            desc="Results ready.",
        )

        return "\n".join(output)

    # -------------------------------------------------------------
    # Gradio Interface
    # -------------------------------------------------------------
    # This is the visible user interface.
    #
    # The interface:
    #   - Receives a search query.
    #   - Calls format_search_results().
    #   - Displays the returned Markdown.
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