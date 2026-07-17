"""
Release 008

Retrieval Policy Engine Validation
"""

from retrieval_policy_engine import (
    RetrievalPolicyEngine,
)

engine = RetrievalPolicyEngine(
    similarity_threshold=0.50
)

candidate_chunks = [
    {
        "title": "Nelson Mandela",
        "similarity": 0.91,
    },
    {
        "title": "Shaka Zulu",
        "similarity": 0.62,
    },
    {
        "title": "Mapungubwe",
        "similarity": 0.41,
    },
]

approved = engine.apply(
    candidate_chunks
)

print("Approved Chunks")
print("=" * 40)

for chunk in approved:
    print(
        chunk["title"],
        chunk["similarity"],
    )