"""
Release 008

Retrieval Pipeline Validation
"""

from sentence_transformers import SentenceTransformer

from embedding_engine import EmbeddingEngine
from retrieval_policy_engine import RetrievalPolicyEngine
from settings import (
    EMBEDDING_MODEL_NAME,
    SIMILARITY_THRESHOLD,
)
from vector_database_engine import VectorDatabaseEngine


print("=" * 60)
print("Loading embedding model...")
print("=" * 60)

model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

embedding_engine = EmbeddingEngine(
    model=model
)

vector_database_engine = VectorDatabaseEngine()

retrieval_policy_engine = RetrievalPolicyEngine(
    similarity_threshold=SIMILARITY_THRESHOLD,
)

print("Embedding model loaded.\n")

# ----------------------------------------------------
# Sample Heritage Knowledge
# ----------------------------------------------------

chunks = [
    {
        "title": "Nelson Mandela",
        "content": (
            "Nelson Mandela became South Africa's "
            "first democratically elected president "
            "after spending 27 years in prison."
        ),
    },
    {
        "title": "Shaka Zulu",
        "content": (
            "Shaka Zulu united and strengthened "
            "the Zulu Kingdom."
        ),
    },
    {
        "title": "Charlotte Maxeke",
        "content": (
            "Charlotte Maxeke was an educator "
            "and women's rights activist."
        ),
    },
]

print("Generating embeddings...")

embedded_chunks = embedding_engine.embed_chunks(
    chunks
)

print("Building vector index...")

vector_database_engine.build_index(
    embedded_chunks
)

query = "Leader imprisoned for 27 years"

print(f"\nQuery: {query}\n")

query_embedding = embedding_engine.embed_text(
    query
)

candidate_chunks = vector_database_engine.search(
    query_embedding=query_embedding,
    top_k=5,
)

print("=" * 60)
print("Candidate Chunks")
print("=" * 60)

for chunk in candidate_chunks:
    print(
        f"{chunk['title']} "
        f"({chunk['similarity']:.4f})"
    )

approved_chunks = retrieval_policy_engine.apply(
    candidate_chunks
)

print("\n")
print("=" * 60)
print("Approved Chunks")
print("=" * 60)

for chunk in approved_chunks:
    print(
        f"{chunk['title']} "
        f"({chunk['similarity']:.4f})"
    )