"""
Release 009

Context Engine Validation
"""

from context_engine import ContextEngine


context_engine = ContextEngine()

approved_chunks = [
    {
        "title": "Nelson Mandela",
        "source": "nelson-mandela.md",
        "content": (
            "Nelson Mandela spent 27 years in prison "
            "before becoming South Africa's first "
            "democratically elected president."
        ),
        "similarity": 0.9214,
    },
    {
        "title": "Robben Island",
        "source": "robben-island.md",
        "content": (
            "Robben Island was used as a prison "
            "during apartheid and held several "
            "political prisoners."
        ),
        "similarity": 0.8126,
    },
]

context = context_engine.build_context(
    approved_chunks=approved_chunks
)

print("=" * 60)
print("LLM-Ready Context")
print("=" * 60)
print(context)
print("=" * 60)

assert isinstance(context, str)
assert "Nelson Mandela" in context
assert "Robben Island" in context
assert "0.9214" in context
assert "---" in context

empty_context = context_engine.build_context(
    approved_chunks=[]
)

assert empty_context == ""

print("\nContext Engine validation passed.")