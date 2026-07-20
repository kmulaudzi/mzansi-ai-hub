"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine

Unit Tests
"""

import pytest

from response_generation_engine import ResponseGenerationEngine


# ---------------------------------------------------------
# Test Doubles
# ---------------------------------------------------------


class FakeTokenizer:
    """
    Small tokenizer replacement used for isolated tests.

    It records the prompt received by the engine and returns
    predictable model inputs.
    """

    def __init__(self):
        self.last_prompt = None

    def __call__(
        self,
        text,
        return_tensors=None,
        truncation=None,
    ):
        self.last_prompt = text

        return {
            "input_ids": [[1, 2, 3]],
            "attention_mask": [[1, 1, 1]],
        }

    def decode(
        self,
        generated_tokens,
        skip_special_tokens=True,
    ):
        return "Shaka Zulu was a leader of the Zulu Kingdom."


class FakeModel:
    """
    Small language-model replacement used for isolated tests.

    It records the arguments passed to generate().
    """

    def __init__(self):
        self.last_generate_arguments = None

    def generate(self, **kwargs):
        self.last_generate_arguments = kwargs

        return [[10, 20, 30]]


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def fake_model():
    return FakeModel()


@pytest.fixture
def fake_tokenizer():
    return FakeTokenizer()


@pytest.fixture
def response_engine(
    fake_model,
    fake_tokenizer,
):
    return ResponseGenerationEngine(
        model=fake_model,
        tokenizer=fake_tokenizer,
        max_new_tokens=100,
        temperature=0.3,
        do_sample=False,
    )


# ---------------------------------------------------------
# Constructor Tests
# ---------------------------------------------------------


def test_engine_requires_model(fake_tokenizer):
    with pytest.raises(
        ValueError,
        match="requires a model",
    ):
        ResponseGenerationEngine(
            model=None,
            tokenizer=fake_tokenizer,
        )


def test_engine_requires_tokenizer(fake_model):
    with pytest.raises(
        ValueError,
        match="requires a tokenizer",
    ):
        ResponseGenerationEngine(
            model=fake_model,
            tokenizer=None,
        )


def test_model_must_have_generate_method(fake_tokenizer):
    invalid_model = object()

    with pytest.raises(
        TypeError,
        match="generate",
    ):
        ResponseGenerationEngine(
            model=invalid_model,
            tokenizer=fake_tokenizer,
        )


def test_tokenizer_must_be_callable(fake_model):
    class InvalidTokenizer:
        def decode(self, tokens, skip_special_tokens=True):
            return "answer"

    with pytest.raises(
        TypeError,
        match="callable",
    ):
        ResponseGenerationEngine(
            model=fake_model,
            tokenizer=InvalidTokenizer(),
        )


def test_tokenizer_must_have_decode_method(fake_model):
    class InvalidTokenizer:
        def __call__(self, text, **kwargs):
            return {}

    with pytest.raises(
        TypeError,
        match="decode",
    ):
        ResponseGenerationEngine(
            model=fake_model,
            tokenizer=InvalidTokenizer(),
        )


def test_max_new_tokens_must_be_positive(
    fake_model,
    fake_tokenizer,
):
    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        ResponseGenerationEngine(
            model=fake_model,
            tokenizer=fake_tokenizer,
            max_new_tokens=0,
        )


def test_temperature_cannot_be_negative(
    fake_model,
    fake_tokenizer,
):
    with pytest.raises(
        ValueError,
        match="cannot be negative",
    ):
        ResponseGenerationEngine(
            model=fake_model,
            tokenizer=fake_tokenizer,
            temperature=-1,
        )


# ---------------------------------------------------------
# Response Generation Tests
# ---------------------------------------------------------


def test_generate_response_returns_decoded_answer(
    response_engine,
):
    answer = response_engine.generate_response(
        query="Who was Shaka Zulu?",
        context=(
            "Shaka Zulu was a leader who played an important "
            "role in the development of the Zulu Kingdom."
        ),
    )

    assert answer == (
        "Shaka Zulu was a leader of the Zulu Kingdom."
    )


def test_generate_response_rejects_empty_query(
    response_engine,
):
    with pytest.raises(
        ValueError,
        match="query must not be empty",
    ):
        response_engine.generate_response(
            query="   ",
            context="Heritage context",
        )


def test_generate_response_returns_fallback_for_empty_context(
    response_engine,
):
    answer = response_engine.generate_response(
        query="Who was Shaka Zulu?",
        context="   ",
    )

    assert answer == (
        "The available heritage knowledge does not contain "
        "enough information to answer this question."
    )


def test_prompt_contains_question_and_context(
    response_engine,
    fake_tokenizer,
):
    response_engine.generate_response(
        query="What is Heritage Day?",
        context="Heritage Day is observed in South Africa.",
    )

    assert "What is Heritage Day?" in fake_tokenizer.last_prompt

    assert (
        "Heritage Day is observed in South Africa."
        in fake_tokenizer.last_prompt
    )


def test_tokenizer_receives_required_arguments(
    response_engine,
    fake_tokenizer,
):
    response_engine.generate_response(
        query="What is Mapungubwe?",
        context="Mapungubwe was an ancient African kingdom.",
    )

    assert fake_tokenizer.last_prompt is not None


def test_model_receives_generation_arguments(
    response_engine,
    fake_model,
):
    response_engine.generate_response(
        query="What is Mapungubwe?",
        context="Mapungubwe was an ancient African kingdom.",
    )

    arguments = fake_model.last_generate_arguments

    assert arguments["max_new_tokens"] == 100
    assert arguments["do_sample"] is False

    assert "input_ids" in arguments
    assert "attention_mask" in arguments


def test_temperature_is_excluded_when_sampling_is_disabled(
    response_engine,
    fake_model,
):
    response_engine.generate_response(
        query="What is Heritage Day?",
        context="Heritage Day celebrates South African heritage.",
    )

    assert (
        "temperature"
        not in fake_model.last_generate_arguments
    )


def test_temperature_is_used_when_sampling_is_enabled(
    fake_model,
    fake_tokenizer,
):
    engine = ResponseGenerationEngine(
        model=fake_model,
        tokenizer=fake_tokenizer,
        temperature=0.7,
        do_sample=True,
    )

    engine.generate_response(
        query="What is Heritage Day?",
        context="Heritage Day celebrates South African heritage.",
    )

    assert (
        fake_model.last_generate_arguments["temperature"]
        == 0.7
    )


def test_empty_model_answer_returns_fallback(
    fake_model,
):
    class EmptyAnswerTokenizer(FakeTokenizer):
        def decode(
            self,
            generated_tokens,
            skip_special_tokens=True,
        ):
            return "   "

    engine = ResponseGenerationEngine(
        model=fake_model,
        tokenizer=EmptyAnswerTokenizer(),
    )

    answer = engine.generate_response(
        query="What is Heritage Day?",
        context="Heritage Day celebrates South African heritage.",
    )

    assert answer == (
        "The available heritage knowledge does not contain "
        "enough information to answer this question."
    )