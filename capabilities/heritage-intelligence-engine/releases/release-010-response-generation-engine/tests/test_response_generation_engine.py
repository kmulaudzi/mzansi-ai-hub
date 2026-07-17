"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine Validation
"""

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from response_generation_engine import ResponseGenerationEngine
from settings import RESPONSE_MODEL_NAME


print("=" * 60)
print("Loading response-generation model...")
print("=" * 60)

# -------------------------------------------------------------
# External Technology Implementation
# -------------------------------------------------------------
#
# Hugging Face creates the tokenizer and model.
#
# These objects are then injected into our own architectural
# contract: ResponseGenerationEngine.
#
# Hugging Face is therefore an implementation detail.
# It is not our application architecture.
# -------------------------------------------------------------

tokenizer = AutoTokenizer.from_pretrained(
    RESPONSE_MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    RESPONSE_MODEL_NAME
)

response_generation_engine = ResponseGenerationEngine(
    model=model,
    tokenizer=tokenizer,
)

print("Model loaded successfully.\n")


# -------------------------------------------------------------
# Test Input
# -------------------------------------------------------------

query = "Why is Robben Island historically significant?"

context = """
Context Item 1
Title: Robben Island
Source: robben-island.md

Robben Island was used as a prison during apartheid.
Several political prisoners were imprisoned there,
including Nelson Mandela.

---

Context Item 2
Title: Nelson Mandela
Source: nelson-mandela.md

Nelson Mandela spent 27 years in prison before becoming
South Africa's first democratically elected president.
"""


# -------------------------------------------------------------
# Generate Response
# -------------------------------------------------------------

response = response_generation_engine.generate_response(
    query=query,
    context=context,
)

print("=" * 60)
print("Question")
print("=" * 60)
print(query)

print("\n")
print("=" * 60)
print("Generated Response")
print("=" * 60)
print(response)
print("=" * 60)


# -------------------------------------------------------------
# Basic Validation
# -------------------------------------------------------------

assert isinstance(response, str)
assert response.strip() != ""

print("\nResponse Generation Engine validation passed.")