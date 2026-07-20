"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine

Real Model Validation
"""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from response_generation_engine import ResponseGenerationEngine
from settings import RESPONSE_MODEL_NAME


def main():
    print(f"Loading model: {RESPONSE_MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(
        RESPONSE_MODEL_NAME
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        RESPONSE_MODEL_NAME
    )

    engine = ResponseGenerationEngine(
        model=model,
        tokenizer=tokenizer,
    )

    question = "Who was Shaka Zulu?"

    context = """
    Shaka Zulu was a major leader of the Zulu Kingdom.
    He played an important role in strengthening and expanding
    the kingdom during the early nineteenth century.
    """

    answer = engine.generate_response(
        query=question,
        context=context,
    )

    print("\nQuestion:")
    print(question)

    print("\nContext:")
    print(context.strip())

    print("\nGenerated Answer:")
    print(answer)


if __name__ == "__main__":
    main()