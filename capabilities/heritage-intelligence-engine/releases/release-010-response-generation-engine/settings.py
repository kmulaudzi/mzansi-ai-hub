"""
Mzansi AI Hub
Heritage Intelligence Engine

Release 010 - Response Generation Engine

Configuration
"""

# ---------------------------------------------------------
# Hugging Face Model
# ---------------------------------------------------------

RESPONSE_MODEL_NAME = "google/flan-t5-base"

# ---------------------------------------------------------
# Generation Parameters
# ---------------------------------------------------------

MAX_NEW_TOKENS = 200

TEMPERATURE = 0.3

DO_SAMPLE = False

# ---------------------------------------------------------
# Prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are the Heritage Intelligence Engine.

Answer ONLY using the supplied heritage context.

If the answer cannot be found in the supplied context,
reply that the available heritage knowledge does not
contain enough information.

Do not invent facts.

Question:
{question}

Context:
{context}

Answer:
""".strip()