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
# RootArc + NHC Presentation Layer
# ============================================================
#
# Public product identity:
#
# National Heritage Council
#        ↓
# Heritage Intelligence
#        ↓
# Powered by RootArc
#
#
# The engineering architecture underneath remains unchanged:
#
# HeritageApplication
#       ↓
# Evidence Retrieval
#       ↓
# Semantic Retrieval
#       ↓
# Response Generation
#
# ============================================================

import html


# ============================================================
# RootArc Visual System
# ============================================================

ROOTARC_CSS = """
/* ==========================================================
   ROOTARC / NHC HERITAGE INTELLIGENCE
   ========================================================== */

:root {
    --rootarc-navy: #001A3A;
    --rootarc-navy-deep: #001128;
    --rootarc-navy-soft: #06254A;

    --rootarc-coral: #FF4D3D;
    --rootarc-coral-light: #FF675B;

    --rootarc-cyan: #16C7D5;
    --rootarc-gold: #F59A00;

    --rootarc-cream: #F7F0E5;
    --rootarc-cream-soft: #FFF9F1;

    --rootarc-text: #F7F0E5;
    --rootarc-dark-text: #071A38;
    --rootarc-muted: #B8C4D5;
}


/* ----------------------------------------------------------
   Entire Gradio canvas
   ---------------------------------------------------------- */

.gradio-container {
    background:
        radial-gradient(
            circle at 50% 0%,
            #062B57 0%,
            #001A3A 38%,
            #001128 100%
        ) !important;

    color: var(--rootarc-text) !important;

    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}


/* ----------------------------------------------------------
   Main application shell
   ---------------------------------------------------------- */

#rootarc-app {
    max-width: 1500px;
    margin: 0 auto;
    padding: 0 34px 60px 34px;
}


/* ----------------------------------------------------------
   Top navigation / identity
   ---------------------------------------------------------- */

.rootarc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 24px 0;

    border-bottom:
        1px solid rgba(255, 255, 255, 0.10);
}

.rootarc-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.rootarc-symbol {
    display: grid;
    place-items: center;

    width: 46px;
    height: 46px;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            var(--rootarc-coral),
            var(--rootarc-gold),
            var(--rootarc-cyan)
        );

    color: white;

    font-size: 24px;
    font-weight: 900;
}

.rootarc-wordmark {
    font-size: 30px;
    font-weight: 900;
    letter-spacing: 1px;
    color: var(--rootarc-cream);
}

.nhc-brand {
    text-align: right;
}

.nhc-name {
    color: var(--rootarc-cream);
    font-weight: 800;
    font-size: 16px;
}

.nhc-sub {
    color: var(--rootarc-muted);
    font-size: 12px;
    margin-top: 3px;
}


/* ----------------------------------------------------------
   Hero
   ---------------------------------------------------------- */

.rootarc-hero {
    text-align: center;
    padding: 64px 20px 30px 20px;
}

.ai-badge {
    display: inline-block;

    padding: 8px 18px;

    border:
        2px solid var(--rootarc-coral);

    border-radius: 9px;

    color: var(--rootarc-coral-light);

    font-size: 13px;
    font-weight: 900;
    letter-spacing: 2px;

    margin-bottom: 24px;
}

.rootarc-hero h1 {
    margin: 0;

    color: var(--rootarc-cream);

    font-size: clamp(
        42px,
        7vw,
        84px
    );

    line-height: 0.95;

    font-weight: 950;

    letter-spacing: 2px;

    text-transform: uppercase;
}

.rootarc-hero .accent {
    color: var(--rootarc-coral);
}

.rootarc-hero-copy {
    max-width: 760px;

    margin:
        28px auto 0 auto;

    color: #E9E4DD;

    font-size: 19px;
    line-height: 1.55;
}

.rootarc-powered {
    margin-top: 16px;

    color: var(--rootarc-muted);

    font-size: 13px;
    letter-spacing: 0.7px;
}


/* ----------------------------------------------------------
   Ask panel
   ---------------------------------------------------------- */

.ask-shell {
    max-width: 1050px;

    margin:
        30px auto 0 auto;

    padding: 8px;

    border:
        1px solid rgba(255, 255, 255, 0.16);

    border-radius: 18px;

    background:
        rgba(1, 24, 52, 0.72);

    box-shadow:
        0 20px 60px
        rgba(0, 0, 0, 0.25);
}

#heritage-question textarea {
    background:
        var(--rootarc-cream-soft) !important;

    color:
        var(--rootarc-dark-text) !important;

    border:
        0 !important;

    border-radius:
        12px !important;

    min-height:
        88px !important;

    font-size:
        17px !important;

    padding:
        18px !important;
}

#heritage-question label {
    color:
        var(--rootarc-cream) !important;

    font-weight:
        700 !important;
}


/* ----------------------------------------------------------
   Primary button
   ---------------------------------------------------------- */

#ask-heritage-button {
    background:
        linear-gradient(
            135deg,
            var(--rootarc-coral),
            #FF3A31
        ) !important;

    color:
        white !important;

    border:
        none !important;

    border-radius:
        11px !important;

    min-height:
        54px !important;

    font-size:
        17px !important;

    font-weight:
        850 !important;

    box-shadow:
        0 8px 22px
        rgba(255, 77, 61, 0.28);
}

#ask-heritage-button:hover {
    transform:
        translateY(-1px);

    filter:
        brightness(1.07);
}


/* ----------------------------------------------------------
   Explore prompts
   ---------------------------------------------------------- */

.explore-label {
    margin-top:
        28px;

    margin-bottom:
        12px;

    color:
        var(--rootarc-cream);

    font-size:
        14px;

    font-weight:
        900;

    letter-spacing:
        1.4px;
}

.prompt-chip button {
    background:
        transparent !important;

    color:
        var(--rootarc-cream) !important;

    border:
        1px solid
        rgba(247, 240, 229, 0.55) !important;

    border-radius:
        9px !important;

    font-size:
        13px !important;

    font-weight:
        650 !important;
}

.prompt-chip button:hover {
    border-color:
        var(--rootarc-cyan) !important;

    color:
        var(--rootarc-cyan) !important;
}


/* ----------------------------------------------------------
   Section headers
   ---------------------------------------------------------- */

.product-section-title {
    margin-top:
        50px;

    margin-bottom:
        14px;

    color:
        var(--rootarc-cream);

    font-weight:
        950;

    font-size:
        24px;

    letter-spacing:
        1px;
}


/* ----------------------------------------------------------
   Answer card
   ---------------------------------------------------------- */

.answer-card {
    padding:
        8px;

    border-radius:
        16px;

    background:
        linear-gradient(
            90deg,
            var(--rootarc-coral),
            var(--rootarc-cyan)
        );
}

#heritage-answer {
    background:
        var(--rootarc-cream) !important;

    color:
        var(--rootarc-dark-text) !important;

    border-radius:
        12px !important;

    padding:
        26px 30px !important;

    min-height:
        150px;

    font-size:
        16px;

    line-height:
        1.65;
}

#heritage-answer p,
#heritage-answer li,
#heritage-answer strong,
#heritage-answer h1,
#heritage-answer h2,
#heritage-answer h3 {
    color:
        var(--rootarc-dark-text) !important;
}


/* ----------------------------------------------------------
   Evidence
   ---------------------------------------------------------- */

.evidence-heading {
    display:
        flex;

    justify-content:
        space-between;

    align-items:
        end;

    gap:
        20px;

    margin-top:
        50px;

    margin-bottom:
        16px;
}

.evidence-heading h2 {
    margin:
        0;

    color:
        var(--rootarc-cream);

    font-size:
        24px;

    font-weight:
        950;

    letter-spacing:
        1px;
}

.evidence-heading p {
    margin:
        0;

    color:
        var(--rootarc-muted);

    font-size:
        13px;
}

.heritage-evidence-grid {
    display:
        grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(240px, 1fr)
        );

    gap:
        14px;
}

.evidence-card {
    position:
        relative;

    background:
        var(--rootarc-cream);

    color:
        var(--rootarc-dark-text);

    border-radius:
        13px;

    padding:
        20px;

    border-top:
        5px solid
        var(--rootarc-cyan);

    min-height:
        150px;
}

.evidence-number {
    color:
        var(--rootarc-coral);

    font-size:
        12px;

    font-weight:
        950;

    letter-spacing:
        1px;
}

.evidence-title {
    margin-top:
        8px;

    color:
        var(--rootarc-dark-text);

    font-size:
        17px;

    font-weight:
        850;
}

.evidence-meta {
    margin-top:
        14px;

    color:
        #43506A;

    font-size:
        12px;

    line-height:
        1.6;
}

.relevance-pill {
    display:
        inline-block;

    margin-top:
        12px;

    padding:
        5px 9px;

    border-radius:
        6px;

    background:
        var(--rootarc-navy);

    color:
        var(--rootarc-cream);

    font-size:
        11px;

    font-weight:
        750;
}


/* ----------------------------------------------------------
   Institutional trust strip
   ---------------------------------------------------------- */

.nhc-trust-strip {
    margin-top:
        44px;

    padding:
        24px;

    border:
        1px solid
        rgba(245, 154, 0, 0.45);

    border-radius:
        14px;

    background:
        rgba(245, 154, 0, 0.06);

    text-align:
        center;
}

.nhc-trust-title {
    color:
        var(--rootarc-gold);

    font-weight:
        900;

    letter-spacing:
        1.1px;
}

.nhc-trust-copy {
    margin-top:
        7px;

    color:
        var(--rootarc-muted);

    font-size:
        13px;
}


/* ----------------------------------------------------------
   Footer
   ---------------------------------------------------------- */

.rootarc-footer {
    margin-top:
        50px;

    padding:
        28px 0;

    border-top:
        1px solid
        rgba(255, 255, 255, 0.10);

    text-align:
        center;

    color:
        #8394AD;

    font-size:
        12px;
}


/* ----------------------------------------------------------
   Hide some default Gradio chrome
   ---------------------------------------------------------- */

footer {
    display:
        none !important;
}


/* ----------------------------------------------------------
   Mobile
   ---------------------------------------------------------- */

@media (
    max-width: 700px
) {

    #rootarc-app {
        padding:
            0 16px 40px 16px;
    }

    .rootarc-header {
        align-items:
            flex-start;
    }

    .rootarc-wordmark {
        font-size:
            23px;
    }

    .nhc-name {
        font-size:
            12px;
    }

    .rootarc-hero {
        padding-top:
            44px;
    }

    .rootarc-hero-copy {
        font-size:
            16px;
    }

    .evidence-heading {
        display:
            block;
    }

    .evidence-heading p {
        margin-top:
            5px;
    }
}
"""


# ============================================================
# Heritage Evidence Formatting
# ============================================================


def format_sources(
    sources,
):
    """
    Convert clean application source metadata into
    RootArc-styled heritage evidence cards.
    """

    if not sources:
        return """
        <div class="heritage-evidence-grid">
            <div class="evidence-card">
                <div class="evidence-title">
                    No supporting sources returned.
                </div>
            </div>
        </div>
        """

    cards = []

    for index, source in enumerate(
        sources,
        start=1,
    ):
        title = html.escape(
            str(
                source.get(
                    "title",
                    "Unknown source",
                )
            )
        )

        filename = html.escape(
            str(
                source.get(
                    "filename",
                    "",
                )
            )
        )

        page_number = source.get(
            "page_number"
        )

        similarity = float(
            source.get(
                "similarity",
                0.0,
            )
        )

        page_html = ""

        if page_number is not None:
            page_html = (
                f"<div>"
                f"<strong>Page:</strong> "
                f"{html.escape(str(page_number))}"
                f"</div>"
            )

        filename_html = ""

        if filename:
            filename_html = (
                f"<div>"
                f"<strong>File:</strong> "
                f"{filename}"
                f"</div>"
            )

        cards.append(
            f"""
            <div class="evidence-card">

                <div class="evidence-number">
                    EVIDENCE {index:02d}
                </div>

                <div class="evidence-title">
                    {title}
                </div>

                <div class="evidence-meta">
                    {filename_html}
                    {page_html}
                </div>

                <div class="relevance-pill">
                    Semantic relevance:
                    {similarity:.2f}
                </div>

            </div>
            """
        )

    return (
        '<div class="heritage-evidence-grid">'
        + "".join(cards)
        + "</div>"
    )


# ============================================================
# Gradio Adapter
# ============================================================


def ask_heritage(
    question: str,
    progress=gr.Progress(),
):
    """
    Send a user question through the complete
    Heritage Intelligence Engine.

    Gradio remains a presentation adapter only.

    Runtime:
        User
          ↓
        HeritageApplication.ask()
          ↓
        Evidence Retrieval
          ↓
        Semantic Retrieval
          ↓
        Response Generation
          ↓
        Answer + Heritage Evidence
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
            desc=(
                "Searching trusted heritage "
                "knowledge..."
            ),
        )

        response = heritage_application.ask(
            question
        )

        progress(
            0.90,
            desc="Preparing heritage evidence...",
        )

        answer = response.get(
            "answer",
            "",
        )

        evidence_html = format_sources(
            response.get(
                "sources",
                [],
            )
        )

        progress(
            1.0,
            desc="Heritage response ready.",
        )

        return (
            answer,
            evidence_html,
        )

    except Exception as error:

        return (
            (
                "### Heritage Intelligence Error\n\n"
                "The request could not be completed.\n\n"
                f"`{type(error).__name__}: {error}`"
            ),
            "",
        )


# ============================================================
# Gradio Interface
# ============================================================

with gr.Blocks(
    title=(
        "NHC Heritage Intelligence — RootArc"
    ),
    css=ROOTARC_CSS,
) as demo:

    with gr.Column(
        elem_id="rootarc-app"
    ):

        # --------------------------------------------------------
        # Product header
        # --------------------------------------------------------

        gr.HTML(
            """
            <div class="rootarc-header">

                <div class="rootarc-brand">

                    <div class="rootarc-symbol">
                        ✦
                    </div>

                    <div class="rootarc-wordmark">
                        RootArc
                    </div>

                </div>

                <div class="nhc-brand">

                    <div class="nhc-name">
                        NATIONAL HERITAGE COUNCIL
                    </div>

                    <div class="nhc-sub">
                        South Africa
                    </div>

                </div>

            </div>
            """
        )

        # --------------------------------------------------------
        # Hero
        # --------------------------------------------------------

        gr.HTML(
            """
            <section class="rootarc-hero">

                <div class="ai-badge">
                    AI-POWERED HERITAGE EXPERIENCE
                </div>

                <h1>
                    HERITAGE
                    <span class="accent">INTELLIGENCE.</span>
                </h1>

                <div class="rootarc-hero-copy">

                    Explore South Africa's heritage through
                    trusted knowledge, stories, places,
                    people and cultural history.

                </div>

                <div class="rootarc-powered">

                    A National Heritage Council product
                    • Powered by RootArc

                </div>

            </section>
            """
        )

        # --------------------------------------------------------
        # Ask
        # --------------------------------------------------------

        with gr.Column(
            elem_classes=[
                "ask-shell"
            ]
        ):

            question_input = gr.Textbox(
                label="Ask about South African heritage",
                placeholder=(
                    "What would you like to discover?"
                ),
                lines=2,
                elem_id="heritage-question",
            )

            ask_button = gr.Button(
                "ASK HERITAGE AI  →",
                variant="primary",
                elem_id="ask-heritage-button",
            )

        # --------------------------------------------------------
        # Prompt shortcuts
        # --------------------------------------------------------

        gr.HTML(
            """
            <div class="explore-label">
                EXPLORE OUR HERITAGE
            </div>
            """
        )

        with gr.Row():

            mapungubwe_button = gr.Button(
                "Mapungubwe",
                elem_classes=[
                    "prompt-chip"
                ],
            )

            robben_button = gr.Button(
                "Robben Island",
                elem_classes=[
                    "prompt-chip"
                ],
            )

            charlotte_button = gr.Button(
                "Charlotte Maxeke",
                elem_classes=[
                    "prompt-chip"
                ],
            )

            cradle_button = gr.Button(
                "Cradle of Humankind",
                elem_classes=[
                    "prompt-chip"
                ],
            )

            ndebele_button = gr.Button(
                "Ndebele Art",
                elem_classes=[
                    "prompt-chip"
                ],
            )

        # --------------------------------------------------------
        # Answer
        # --------------------------------------------------------

        gr.HTML(
            """
            <div class="product-section-title">
                ANSWER
            </div>
            """
        )

        with gr.Column(
            elem_classes=[
                "answer-card"
            ]
        ):

            answer_output = gr.Markdown(
                elem_id="heritage-answer"
            )

        # --------------------------------------------------------
        # Heritage Evidence
        # --------------------------------------------------------

        gr.HTML(
            """
            <div class="evidence-heading">

                <div>
                    <h2>
                        HERITAGE EVIDENCE
                    </h2>

                    <p>
                        Supporting knowledge used to ground
                        this response.
                    </p>
                </div>

            </div>
            """
        )

        sources_output = gr.HTML()

        # --------------------------------------------------------
        # Trust / ownership
        # --------------------------------------------------------

        gr.HTML(
            """
            <div class="nhc-trust-strip">

                <div class="nhc-trust-title">
                    NATIONAL HERITAGE COUNCIL
                </div>

                <div class="nhc-trust-copy">

                    Heritage Intelligence is designed to
                    support responsible access to South
                    African heritage knowledge.

                    Responses are grounded in configured
                    heritage evidence rather than relying
                    solely on general-purpose AI knowledge.

                </div>

            </div>
            """
        )

        gr.HTML(
            """
            <div class="rootarc-footer">

                National Heritage Council
                • Heritage Intelligence
                • Powered by RootArc

            </div>
            """
        )


    # ========================================================
    # Standard Question Submission
    # ========================================================

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


    # ========================================================
    # Exploration Shortcuts
    # ========================================================

    mapungubwe_button.click(
        fn=lambda: (
            "Tell me about Mapungubwe"
        ),
        outputs=question_input,
    ).then(
        fn=ask_heritage,
        inputs=question_input,
        outputs=[
            answer_output,
            sources_output,
        ],
    )

    robben_button.click(
        fn=lambda: (
            "What is the significance of Robben Island?"
        ),
        outputs=question_input,
    ).then(
        fn=ask_heritage,
        inputs=question_input,
        outputs=[
            answer_output,
            sources_output,
        ],
    )

    charlotte_button.click(
        fn=lambda: (
            "Who was Charlotte Maxeke?"
        ),
        outputs=question_input,
    ).then(
        fn=ask_heritage,
        inputs=question_input,
        outputs=[
            answer_output,
            sources_output,
        ],
    )

    cradle_button.click(
        fn=lambda: (
            "What is the Cradle of Humankind?"
        ),
        outputs=question_input,
    ).then(
        fn=ask_heritage,
        inputs=question_input,
        outputs=[
            answer_output,
            sources_output,
        ],
    )

    ndebele_button.click(
        fn=lambda: (
            "Tell me about Ndebele art"
        ),
        outputs=question_input,
    ).then(
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
# enables queued execution and visible progress.
#
# share=True
# gives Colab a temporary public demo URL.
#
# ============================================================

if __name__ == "__main__":

    demo.queue()

    demo.launch(
        share=True,
    )