"""
Release 007

Vector Database Engine Validation
"""

from sentence_transformers import SentenceTransformer

from embedding_engine import EmbeddingEngine
from settings import EMBEDDING_MODEL_NAME
from vector_database_engine import (
    VectorDatabaseEngine,
)

print("=" * 60)
print("Loading embedding model...")
print("=" * 60)

model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

embedding_engine = EmbeddingEngine(
    model=model
)

vector_database = VectorDatabaseEngine()

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

print("Generating chunk embeddings...")

embedded_chunks = embedding_engine.embed_chunks(
    chunks=chunks
)

print(
    f"{len(embedded_chunks)} chunks embedded.\n"
)

print("Building FAISS index...")

vector_database.build_index(
    embedded_chunks
)

print("Vector index ready.\n")

query = "Leader imprisoned for 27 years"

print(f"Query: {query}\n")

query_embedding = embedding_engine.embed_text(
    query
)

results = vector_database.search(
    query_embedding=query_embedding,
    top_k=3,
)

print("=" * 60)
print("Nearest Neighbours")
print("=" * 60)

for index, result in enumerate(
    results,
    start=1,
):
    print(f"{index}. {result['title']}")
    print(
        f"Similarity : "
        f"{result['similarity']:.4f}"
    )
    print()