"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 006 - Semantic Search Engine

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
from similarity_engine import SimilarityEngine


def create_demo(
    embedding_model: Any,
) -> gr.Interface:
    """
    Build the complete Release 006 application.

    Runtime flow
    ------------
    1. Colab loads the Hugging Face embedding model.
    2. Colab passes the model into create_demo().
    3. This function creates the document Providers.
    4. It creates the Chunking Engine.
    5. It connects the Hugging Face model to our Embedding Engine.
    6. It creates the stateless Similarity Engine.
    7. It connects everything through the Application Engine.
    8. It prepares and caches the heritage knowledge once.
    9. It creates and returns the Gradio interface.
    """

    # -------------------------------------------------------------
    # Provider Layer
    # -------------------------------------------------------------
    # Providers read different source formats and convert them into
    # the same standard document structure.
    #
    # MarkdownProvider:
    #   Reads the structured Knowledge Cards.
    #
    # PDFProvider:
    #   Reads the heritage PDF collection.
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
    # The Chunking Engine divides large documents into smaller
    # pieces of knowledge.
    #
    # Each chunk preserves:
    #   - Source file
    #   - Source type
    #   - Parent document
    #   - Chunk ID
    #   - Chunk index
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
    # This is the connection point between:
    #
    # Hugging Face model
    #        ↓
    # Our Embedding Engine
    #        ↓
    # Heritage Intelligence Engine
    #
    # The same engine embeds:
    #   - Document chunks during startup
    #   - User queries during search
    # -------------------------------------------------------------

    embedding_engine = EmbeddingEngine(
        model=embedding_model
    )

    # -------------------------------------------------------------
    # Similarity Layer
    # -------------------------------------------------------------
    # The Similarity Engine compares:
    #
    # User query embedding
    #        +
    # Cached document chunk embeddings
    #
    # It enriches each chunk with a similarity score and returns
    # the chunks sorted from most similar to least similar.
    #
    # It is stateless and performs pure vector mathematics.
    # -------------------------------------------------------------

    similarity_engine = SimilarityEngine()

    # -------------------------------------------------------------
    # Application Layer
    # -------------------------------------------------------------
    # The Application Engine coordinates the complete workflow.
    #
    # It connects:
    #   - Providers
    #   - Chunking Engine
    #   - Embedding Engine
    #   - Similarity Engine
    #   - Retrieval Engine
    #
    # Gradio only communicates with the Application Engine.
    # -------------------------------------------------------------

    application_engine = ApplicationEngine(
        providers=[
            markdown_provider,
            pdf_provider,
        ],
        chunking_engine=chunking_engine,
        embedding_engine=embedding_engine,
        similarity_engine=similarity_engine,
        max_results=MAX_RESULTS,
    )

    # -------------------------------------------------------------
    # Prepare and Cache Heritage Knowledge
    # -------------------------------------------------------------
    # This expensive workflow runs once when create_demo() is called.
    #
    # Startup preparation:
    #
    # Providers
    #     ↓
    # Documents
    #     ↓
    # Chunking Engine
    #     ↓
    # Chunks
    #     ↓
    # Embedding Engine
    #     ↓
    # Embedded chunks cached in memory
    #
    # User searches reuse the cache instead of repeating this work.
    # -------------------------------------------------------------

    print("Preparing heritage knowledge...")
    print(
        "Loading documents, creating chunks and "
        "generating embeddings."
    )

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
    # Search-time flow:
    #
    # User query
    #     ↓
    # Application Engine
    #     ↓
    # Retrieval Engine
    #     ↓
    # Embedding Engine creates query vector
    #     ↓
    # Similarity Engine compares vectors
    #     ↓
    # Semantic matches returned
    #     ↓
    # Gradio formats and displays results
    #
    # Gradio does not perform AI processing itself.
    # -------------------------------------------------------------

    def format_search_results(
        query: str,
        progress=gr.Progress(),
    ) -> str:
        """
        Search the prepared heritage knowledge by semantic meaning.

        Search-time flow
        ----------------
        1. Receive the user's natural-language query.
        2. Convert the query into an embedding.
        3. Compare it with cached chunk embeddings.
        4. Return the most semantically similar chunks.
        5. Format the results for Gradio.
        """

        if not query or not query.strip():
            return "Please enter a search query."

        try:
            progress(
                0.15,
                desc="Receiving search query...",
            )

            progress(
                0.35,
                desc="Converting query into an embedding...",
            )

            progress(
                0.65,
                desc="Comparing semantic meaning...",
            )

            response = application_engine.search(
                query=query
            )

            progress(
                0.85,
                desc="Formatting semantic results...",
            )

        except Exception as error:
            return (
                "## Application error\n\n"
                f"```text\n"
                f"{type(error).__name__}: {error}\n"
                f"```"
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
            (
                "These results were retrieved using semantic "
                "similarity rather than keyword matching."
            ),
            "",
        ]

        for index, result in enumerate(
            response["results"],
            start=1,
        ):
            similarity_score = result.get(
                "similarity",
                0.0,
            )

            output.extend(
                [
                    f"### {index}. {result['title']}",
                    "",
                    (
                        "**Semantic similarity:** "
                        f"`{similarity_score:.4f}`"
                    ),
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
            desc="Semantic results ready.",
        )

        return "\n".join(output)

    # -------------------------------------------------------------
    # Gradio Interface
    # -------------------------------------------------------------
    # The interface:
    #   - Receives a natural-language heritage question.
    #   - Calls format_search_results().
    #   - Displays the returned Markdown.
    #
    # The examples intentionally include queries that do not rely
    # only on exact keywords.
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
        description=(
            f"{APPLICATION_DESCRIPTION}\n\n"
            "Release 006 searches heritage knowledge by meaning."
        ),
        examples=[
            ["South Africa's first democratic president"],
            ["Leader imprisoned for 27 years"],
            ["Women who advanced education and equality"],
            ["Ancient African kingdom known for trade"],
            ["Traditional artwork created by women"],
        ],
    )