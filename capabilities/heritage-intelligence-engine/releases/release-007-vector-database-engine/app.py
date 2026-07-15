"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 007 - Vector Database Engine

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
from vector_database_engine import VectorDatabaseEngine


def create_demo(
    embedding_model: Any,
) -> gr.Interface:
    """
    Build the complete Release 007 application.

    Full runtime flow
    -----------------
    1. Google Colab loads the Hugging Face embedding model.
    2. Colab passes the model into create_demo().
    3. This function creates the document Providers.
    4. It creates the Chunking Engine.
    5. It connects the Hugging Face model to our Embedding Engine.
    6. It creates the Vector Database Engine.
    7. It injects every component into the Application Engine.
    8. The application loads, chunks and embeds the documents.
    9. The Vector Database Engine builds the FAISS index.
    10. The Gradio interface is created and returned.

    app.py is the runtime blueprint.

    It shows where all architectural components are created
    and connected.
    """

    # -------------------------------------------------------------
    # Provider Layer
    # Python:
    # providers/markdown_provider.py
    # providers/pdf_provider.py
    # -------------------------------------------------------------
    #
    # Providers read different source formats and convert them into
    # the same standard document contract.
    #
    # MarkdownProvider:
    #   Reads the structured Heritage Knowledge Cards.
    #
    # PDFProvider:
    #   Reads the heritage PDF collection.
    #
    # Both providers return documents containing fields such as:
    #
    #   filename
    #   title
    #   content
    #   source_type
    #   source_path
    # -------------------------------------------------------------

    markdown_provider = MarkdownProvider(
        source_path=str(DATASET_PATH)
    )

    pdf_provider = PDFProvider(
        source_path=str(PDF_DATASET_PATH)
    )

    # -------------------------------------------------------------
    # Pre-processing Layer
    # Python:
    # chunking_engine.py
    # -------------------------------------------------------------
    #
    # The Chunking Engine divides large documents into smaller
    # searchable pieces of knowledge.
    #
    # It preserves:
    #
    #   source file
    #   source type
    #   source path
    #   parent document
    #   chunk ID
    #   chunk index
    #
    # The overlap helps preserve context between neighbouring chunks.
    # -------------------------------------------------------------

    chunking_engine = ChunkingEngine(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    # -------------------------------------------------------------
    # Embedding Layer
    # Python:
    # embedding_engine.py
    # -------------------------------------------------------------
    #
    # embedding_model is the real Hugging Face model loaded in Colab.
    #
    # EmbeddingEngine is our architectural wrapper around that model.
    #
    # This is the connection point:
    #
    # Hugging Face SentenceTransformer
    #               ↓
    #         EmbeddingEngine
    #               ↓
    # Heritage Intelligence Engine
    #
    # The same Embedding Engine is used for:
    #
    # Startup:
    #   Document chunks → chunk embeddings
    #
    # Search time:
    #   User query → query embedding
    #
    # Sentence Transformers remains an implementation behind
    # our stable Embedding Engine contract.
    # -------------------------------------------------------------

    embedding_engine = EmbeddingEngine(
        model=embedding_model
    )

    # -------------------------------------------------------------
    # Intelligence Storage Layer
    # Python:
    # vector_database_engine.py
    # -------------------------------------------------------------
    #
    # The Vector Database Engine owns the AI memory layer.
    #
    # Startup:
    #
    # Embedded chunks
    #       ↓
    # build_index()
    #       ↓
    # FAISS vector index
    #
    # Search time:
    #
    # Query embedding
    #       ↓
    # search()
    #       ↓
    # Nearest-neighbour chunks
    #
    # FAISS is only the implementation behind our contract.
    #
    # The rest of the application does not import or communicate
    # with FAISS directly.
    # -------------------------------------------------------------

    vector_database_engine = VectorDatabaseEngine()

    # -------------------------------------------------------------
    # Application Layer
    # Python:
    # application_engine.py
    # -------------------------------------------------------------
    #
    # The Application Engine coordinates the user-facing workflow.
    #
    # It receives:
    #
    #   Providers
    #   Chunking Engine
    #   Embedding Engine
    #   Vector Database Engine
    #
    # It injects these components into the Retrieval Engine.
    #
    # Gradio communicates only with the Application Engine.
    # -------------------------------------------------------------

    application_engine = ApplicationEngine(
        providers=[
            markdown_provider,
            pdf_provider,
        ],
        chunking_engine=chunking_engine,
        embedding_engine=embedding_engine,
        vector_database_engine=vector_database_engine,
        max_results=MAX_RESULTS,
    )

    # -------------------------------------------------------------
    # Startup Preparation
    # -------------------------------------------------------------
    #
    # This expensive workflow runs once when create_demo() is called.
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
    # Searches reuse the existing index.
    #
    # The complete document preparation pipeline does not run again
    # for every user query.
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
    # Python:
    # app.py
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
    # Embedding Engine.embed_text()
    #     ↓
    # Query embedding
    #     ↓
    # VectorDatabaseEngine.search()
    #     ↓
    # FAISS nearest neighbours
    #     ↓
    # Enriched heritage chunks
    #     ↓
    # Gradio Markdown output
    #
    # Gradio does not:
    #
    #   load documents
    #   create chunks
    #   generate embeddings
    #   build indexes
    #   search FAISS directly
    #
    # It only receives user input and displays application output.
    # -------------------------------------------------------------

    def format_search_results(
        query: str,
        progress=gr.Progress(),
    ) -> str:
        """
        Search the FAISS heritage index and format the results.

        Search-time flow
        ----------------
        1. Receive the user's natural-language query.
        2. Convert the query into an embedding.
        3. Search the FAISS vector index.
        4. Retrieve the nearest embedded chunks.
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
                desc="Searching the heritage vector index...",
            )

            response = application_engine.search(
                query=query
            )

            progress(
                0.85,
                desc="Formatting nearest-neighbour results...",
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
                "These results were retrieved from the FAISS "
                "vector index using semantic nearest-neighbour search."
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
            desc="Nearest-neighbour results ready.",
        )

        return "\n".join(output)

    # -------------------------------------------------------------
    # Gradio Interface
    # -------------------------------------------------------------
    #
    # The examples intentionally use meaning-based queries rather
    # than only exact document keywords.
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
            "Release 007 stores heritage meaning in a FAISS "
            "vector index and retrieves the nearest neighbours."
        ),
        examples=[
            ["South Africa's first democratic president"],
            ["Leader imprisoned for 27 years"],
            ["Women who advanced education and equality"],
            ["Ancient African kingdom known for trade"],
            ["Traditional artwork created by women"],
        ],
    )