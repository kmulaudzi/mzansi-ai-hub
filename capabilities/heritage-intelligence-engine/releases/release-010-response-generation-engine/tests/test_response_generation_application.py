"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Application

Unit Tests
"""

import pytest

from response_generation_application import (
    ResponseGenerationApplication,
)


# ---------------------------------------------------------
# Test Double
# ---------------------------------------------------------


class FakeResponseGenerationEngine:
    """
    Small engine replacement used to test orchestration.

    It records the values received from the application and
    returns a predictable answer.
    """

    def __init__(self):
        self.last_query = None
        self.last_context = None

    def generate_response(
        self,
        query: str,
        context: str,
    ) -> str:
        self.last_query = query
        self.last_context = context

        return "Shaka Zulu was a major leader of the Zulu Kingdom."


# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def fake_engine():
    return FakeResponseGenerationEngine()


@pytest.fixture
def application(fake_engine):
    return ResponseGenerationApplication(
        response_generation_engine=fake_engine,
    )


# ---------------------------------------------------------
# Constructor Tests
# ---------------------------------------------------------


def test_application_stores_response_generation_engine(
    application,
    fake_engine,
):
    assert application.response_generation_engine is fake_engine


# ---------------------------------------------------------
# Execution Tests
# ---------------------------------------------------------


def test_execute_calls_response_generation_engine(
    application,
    fake_engine,
):
    question = "Who was Shaka Zulu?"

    context = (
        "Shaka Zulu was a major leader of the Zulu Kingdom."
    )

    application.execute(
        question=question,
        context=context,
    )

    assert fake_engine.last_query == question
    assert fake_engine.last_context == context


def test_execute_returns_successful_result(application):
    result = application.execute(
        question="Who was Shaka Zulu?",
        context=(
            "Shaka Zulu was a major leader of the Zulu Kingdom."
        ),
    )

    assert result["success"] is True


def test_execute_returns_capability_name(application):
    result = application.execute(
        question="What is Heritage Day?",
        context=(
            "Heritage Day celebrates South African heritage."
        ),
    )

    assert result["capability"] == "Knowledge Communication"


def test_execute_returns_release_number(application):
    result = application.execute(
        question="What is Mapungubwe?",
        context=(
            "Mapungubwe was an ancient African kingdom."
        ),
    )

    assert result["release"] == "010"


def test_execute_returns_original_question(application):
    question = "What is Mapungubwe?"

    result = application.execute(
        question=question,
        context=(
            "Mapungubwe was an ancient African kingdom."
        ),
    )

    assert result["question"] == question


def test_execute_returns_original_context(application):
    context = "Mapungubwe was an ancient African kingdom."

    result = application.execute(
        question="What is Mapungubwe?",
        context=context,
    )

    assert result["context"] == context


def test_execute_returns_generated_answer(application):
    result = application.execute(
        question="Who was Shaka Zulu?",
        context=(
            "Shaka Zulu was a major leader of the Zulu Kingdom."
        ),
    )

    assert result["answer"] == (
        "Shaka Zulu was a major leader of the Zulu Kingdom."
    )


def test_execute_returns_confidence_placeholder(application):
    result = application.execute(
        question="What is Heritage Day?",
        context=(
            "Heritage Day celebrates South African heritage."
        ),
    )

    assert result["confidence"] is None


def test_result_contains_expected_contract_fields(application):
    result = application.execute(
        question="What is Heritage Day?",
        context=(
            "Heritage Day celebrates South African heritage."
        ),
    )

    assert set(result.keys()) == {
        "success",
        "capability",
        "release",
        "question",
        "context",
        "answer",
        "confidence",
    }


def test_engine_errors_are_not_hidden():
    class FailingEngine:
        def generate_response(
            self,
            query: str,
            context: str,
        ) -> str:
            raise ValueError("The query must not be empty.")

    application = ResponseGenerationApplication(
        response_generation_engine=FailingEngine(),
    )

    with pytest.raises(
        ValueError,
        match="query must not be empty",
    ):
        application.execute(
            question="",
            context="Heritage context",
        )