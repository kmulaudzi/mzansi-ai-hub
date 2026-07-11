##%%writefile app.py
import os
import sys

if "COLAB_RELEASE_TAG" not in os.environ:
    sys.exit(
        "Release 001 is configured to run in Google Colab only. "
        "Open the project in Colab to launch the Heritage Intelligence Engine."
    )


import gradio as gr

from ai_response_generator import MzansiAIAssistant

assistant = MzansiAIAssistant()


def respond(question):

    if not question.strip():
        return "Please enter a heritage question."

    return assistant.ask(question)


demo = gr.Interface(
    fn=respond,

    inputs=gr.Textbox(
        lines=2,
        placeholder="Ask a question about South African heritage..."
    ),

    outputs=gr.Textbox(lines=10),

    title="🇿🇦 Mzansi AI Hub",

    description="""
Release 001

Heritage Knowledge Assistant

This prototype searches a Foundation Heritage Dataset before asking an AI model to generate an answer.

Current Version:
• Foundation Knowledge Cards
• Keyword Search
• Prompt Builder
• FLAN-T5 Base
""",

    examples=[
        ["Who was Nelson Mandela?"],
        ["What is Mapungubwe?"],
        ["Tell me about Heritage Day"],
        ["Who was Shaka Zulu?"]
    ]
)


if __name__ == "__main__":
    demo.launch(share=True)