"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 008 - Semantic Retrieval Engine

Gradio Presentation Adapter and Runtime Blueprint
"""

from typing import Any

import gradio as gr

from bootstrap import create_application
from settings import (
    APPLICATION_DESCRIPTION,
    APPLICATION_NAME,
    RESULTS_LABEL,
    SEARCH_LABEL,
    SEARCH_PLACEHOLDER,
    WINDOW_TITLE,
)


def create_demo(
    embedding_model: Any,
) -> gr.Interface:
    """
    Build and return the Release 008 Gradio application.

    Runtime flow
    ------------
    1. Google Colab loads the external embedding model.
    2. Colab passes the model into create_demo().
    3. bootstrap.py assembles the Semantic Retrieval capability.
    4. The Application Engine prepares the heritage knowledge index.
    5. Gradio sends user queries to the Application Engine.
    6. The Application Engine returns approved semantic results.
    7. Gradio formats and displays the retrieved evidence.

    Responsibility
    --------------
    app.py owns the presentation layer.

    It does not construct the internal retrieval components directly.
    Capability assembly belongs to bootstrap.py.
    """

    # -------------------------------------------------------------
    # Capability Bootstrap
    # Python:
    # bootstrap.py
    # -------------------------------------------------------------
    #
    # bootstrap.py creates and connects:
    #
    #   Markdown Provider
    #   PDF Provider
    #   Chunking Engine
    #   Embedding Engine
    #   Vector Database Engine
    #   Retrieval Policy Engine
    #   Application Engine
    #
    # app.py receives only the completed Application Engine.
    # -------------------------------------------------------------

    application_engine = create_application(
        embedding_model=embedding_model,
    )

    # -------------------------------------------------------------
    # Startup Preparation
    # -------------------------------------------------------------
    #
    # This workflow runs once when create_demo() is called.
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
    # Embedded chunks
    #     ↓
    # Vector Database Engine
    #     ↓
    # FAISS vector index
    #
    # User searches reuse the prepared index.
    # -------------------------------------------------------------

    print("Preparing heritage intelligence...")
    print(
        "Loading documents, creating chunks, generating embeddings "
        "and building the FAISS vector index."
    )

    indexed_chunk_count = application_engine.prepare()

    print(
        f"Heritage intelligence ready. "
        f"Indexed {indexed_chunk_count} embedded chunks."
    )

    # -------------------------------------------------------------
    # Presentation Adapter
    # -------------------------------------------------------------
    #
    # Gradio receives the user query and sends it to the
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
    # Query embedding
    #     ↓
    # Vector Database search
    #     ↓
    # Retrieval policy
    #     ↓
    # Approved semantic results
    #     ↓
    # Gradio Markdown output
    #
    # Gradio does not:
    #
    #   load documents
    #   create chunks
    #   generate embeddings directly
    #   build the FAISS index directly
    #   apply retrieval policies directly
    #
    # It only receives input and displays application output.
    # -------------------------------------------------------------

    def format_search_results(
        query: str,
        progress=gr.Progress(),
    ) -> str:
        """
        Search the heritage knowledge index and format the results.

        Parameters
        ----------
        query:
            Natural-language heritage search query.

        progress:
            Gradio progress indicator.

        Returns
        -------
        str
            Markdown-formatted semantic retrieval results.
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
                desc="Searching the heritage vector index...",
            )

            response = application_engine.search(
                query=query,
            )

            progress(
                0.85,
                desc="Formatting semantic retrieval results...",
            )

        except Exception as error:
            return (
                "## Application error\n\n"
                "```text\n"
                f"{type(error).__name__}: {error}\n"
                "```"
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
                "These results were retrieved from the heritage "
                "vector index using semantic similarity search."
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

            vector_index = result.get(
                "vector_index",
                "Unknown",
            )

            output.extend(
                [
                    f"### {index}. {result['title']}",
                    "",
                    (
                        "**Vector similarity:** "
                        f"`{similarity_score:.4f}`"
                    ),
                    "",
                    f"**FAISS vector index:** `{vector_index}`",
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
            desc="Semantic retrieval results ready.",
        )

        return "\n".join(output)

    # -------------------------------------------------------------
    # Gradio Interface
    # -------------------------------------------------------------
    #
    # The examples intentionally use meaning-based queries rather
    # than relying only on exact document keywords.
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
            "Release 008 retrieves relevant heritage evidence using "
            "semantic embeddings, FAISS nearest-neighbour search, "
            "and retrieval policy filtering."
        ),
        examples=[
            ["South Africa's first democratic president"],
            ["Leader imprisoned for 27 years"],
            ["Women who advanced education and equality"],
            ["Ancient African kingdom known for trade"],
            ["Traditional artwork created by women"],
        ],
    )