import gradio as gr

from application_engine import ApplicationEngine
from settings import (
    APPLICATION_DESCRIPTION,
    APPLICATION_NAME,
    DATASET_PATH,
    MAX_RESULTS,
    RESULTS_LABEL,
    SEARCH_LABEL,
    SEARCH_PLACEHOLDER,
    WINDOW_TITLE,
)


# -------------------------------------------------------------------
# Application Engine
# -------------------------------------------------------------------

application_engine = ApplicationEngine(
    dataset_path=str(DATASET_PATH),
    max_results=MAX_RESULTS,
)


# -------------------------------------------------------------------
# Interface Adapter
# -------------------------------------------------------------------

def format_search_results(query: str) -> str:
    """
    Convert the Application Engine response into Markdown
    for the Gradio interface.
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
                f"**Source:** `{result['filename']}`",
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
        ["kingdom"],
        ["women leaders"],
    ],
)


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    demo.launch(share=True)