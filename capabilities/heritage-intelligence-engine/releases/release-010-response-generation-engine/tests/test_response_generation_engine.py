"""
Independent validation for the Response Generation Engine.

Run this test in Google Colab because it loads a Hugging Face model.

Command:

python3 -m tests.test_response_generation_engine
"""

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from response_generation_engine import ResponseGenerationEngine
from settings import (
    MAX_RESPONSE_TOKENS,
    RESPONSE_MODEL_NAME,
)


def print_test_heading(title: str) -> None:
    """
    Print a readable test heading.
    """

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def build_engine() -> ResponseGenerationEngine:
    """
    Load the Hugging Face technology and inject it into
    the Response Generation Engine.
    """

    print(f"\nLoading tokenizer: {RESPONSE_MODEL_NAME}")

    tokenizer = AutoTokenizer.from_pretrained(
        RESPONSE_MODEL_NAME
    )

    print(f"Loading model: {RESPONSE_MODEL_NAME}")

    model = AutoModelForSeq2SeqLM.from_pretrained(
        RESPONSE_MODEL_NAME
    )

    print("Model and tokenizer loaded successfully.")

    return ResponseGenerationEngine(
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MAX_RESPONSE_TOKENS,
    )


def test_grounded_answer(
    engine: ResponseGenerationEngine,
) -> None:
    """
    Test that the model answers using supplied context.
    """

    print_test_heading(
        "TEST 1 - GROUNDED ANSWER"
    )

    query = "Who was Nelson Mandela?"

    context = """
Nelson Mandela was a South African anti-apartheid leader.

He spent 27 years in prison.

In 1994, he became South Africa's first democratically elected President.
""".strip()

    response = engine.generate_response(
        query=query,
        context=context,
    )

    print("\nQuestion:")
    print(query)

    print("\nContext:")
    print(context)

    print("\nGenerated Answer:")
    print(response)

    assert isinstance(response, str)
    assert response.strip() != ""

    response_lower = response.lower()

    assert (
        "mandela" in response_lower
        or "president" in response_lower
        or "anti-apartheid" in response_lower
        or "27 years" in response_lower
    )

    print("\nPASS: The engine returned a grounded answer.")


def test_answer_from_specific_fact(
    engine: ResponseGenerationEngine,
) -> None:
    """
    Test that the engine can answer a direct factual question.
    """

    print_test_heading(
        "TEST 2 - DIRECT FACTUAL ANSWER"
    )

    query = "How long did Nelson Mandela spend in prison?"

    context = """
Nelson Mandela spent 27 years in prison before becoming
South Africa's first democratically elected President.
""".strip()

    response = engine.generate_response(
        query=query,
        context=context,
    )

    print("\nQuestion:")
    print(query)

    print("\nGenerated Answer:")
    print(response)

    assert isinstance(response, str)
    assert response.strip() != ""
    assert "27" in response

    print("\nPASS: The engine used the supplied factual information.")


def test_missing_information(
    engine: ResponseGenerationEngine,
) -> None:
    """
    Test how the model responds when the answer is not present
    in the supplied context.
    """

    print_test_heading(
        "TEST 3 - MISSING INFORMATION"
    )

    query = (
        "How many tourists visit Robben Island every year?"
    )

    context = """
Robben Island is located near Cape Town.

It was used as a prison for political prisoners during apartheid.

Nelson Mandela was imprisoned there.
""".strip()

    response = engine.generate_response(
        query=query,
        context=context,
    )

    print("\nQuestion:")
    print(query)

    print("\nGenerated Answer:")
    print(response)

    assert isinstance(response, str)
    assert response.strip() != ""

    response_lower = response.lower()

    acceptable_phrases = [
        "not contain enough information",
        "does not contain",
        "not provided",
        "not specified",
        "cannot be determined",
        "available heritage documents",
    ]

    assert any(
        phrase in response_lower
        for phrase in acceptable_phrases
    )

    print(
        "\nPASS: The engine did not invent an unsupported visitor number."
    )


def test_empty_context(
    engine: ResponseGenerationEngine,
) -> None:
    """
    Test deterministic behaviour when no context is supplied.
    """

    print_test_heading(
        "TEST 4 - EMPTY CONTEXT"
    )

    response = engine.generate_response(
        query="Who was Shaka Zulu?",
        context="",
    )

    print("\nGenerated Answer:")
    print(response)

    expected_response = (
        "The available heritage documents do not contain "
        "enough information to answer this question."
    )

    assert response == expected_response

    print(
        "\nPASS: Empty context returned the controlled fallback message."
    )


def test_empty_query(
    engine: ResponseGenerationEngine,
) -> None:
    """
    Test that an empty query is rejected.
    """

    print_test_heading(
        "TEST 5 - EMPTY QUERY VALIDATION"
    )

    try:
        engine.generate_response(
            query="",
            context="Some heritage context.",
        )

    except ValueError as error:
        print("\nExpected Error:")
        print(error)

        assert str(error) == "The query cannot be empty."

        print("\nPASS: Empty query was rejected.")
        return

    raise AssertionError(
        "The engine should raise ValueError for an empty query."
    )


def run_tests() -> None:
    """
    Run all Response Generation Engine validation tests.
    """

    print("\n" + "=" * 70)
    print("MZANSI AI HUB")
    print("RELEASE 010A - RESPONSE GENERATION ENGINE")
    print("INDEPENDENT VALIDATION")
    print("=" * 70)

    engine = build_engine()

    test_grounded_answer(engine)
    test_answer_from_specific_fact(engine)
    test_missing_information(engine)
    test_empty_context(engine)
    test_empty_query(engine)

    print("\n" + "=" * 70)
    print("ALL RESPONSE GENERATION ENGINE TESTS PASSED")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()