"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010

Knowledge Communication Capability Demo
"""

import gradio as gr

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)

from settings import (
    RESPONSE_MODEL_NAME,
)

from response_generation_engine import (
    ResponseGenerationEngine,
)

from response_generation_application import (
    ResponseGenerationApplication,
)


# ----------------------------------------------------
# Load Hugging Face Model
# ----------------------------------------------------

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(
    RESPONSE_MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    RESPONSE_MODEL_NAME
)

print("Model loaded successfully.")


# ----------------------------------------------------
# Build Capability
# ----------------------------------------------------

engine = ResponseGenerationEngine(
    model=model,
    tokenizer=tokenizer,
)

application = ResponseGenerationApplication(
    response_generation_engine=engine,
)


# ----------------------------------------------------
# Gradio Function
# ----------------------------------------------------

def generate_answer(question, context):

    result = application.execute(
        question=question,
        context=context,
    )

    return result["answer"]


# ----------------------------------------------------
# User Interface
# ----------------------------------------------------

demo = gr.Interface(
    fn=generate_answer,

    inputs=[
        gr.Textbox(
            label="Question",
            lines=2,
            placeholder="Ask a heritage question..."
        ),

        gr.Textbox(
            label="Context",
            lines=10,
            placeholder="Paste retrieved heritage context here..."
        ),
    ],

    outputs=gr.Textbox(
        label="Generated Answer",
        lines=6,
    ),

    title="Mzansi AI Hub",

    description="""
Knowledge Communication Capability

Release 010

Provide a question together with prepared context.
The AI generates a grounded response using the supplied context.
""",
)

demo.queue()

demo.launch(share=True)