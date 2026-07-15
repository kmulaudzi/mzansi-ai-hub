"""
Release 006

Similarity Engine Validation
"""

from sentence_transformers import SentenceTransformer

from embedding_engine import EmbeddingEngine
from similarity_engine import SimilarityEngine
from settings import EMBEDDING_MODEL_NAME


print("Loading embedding model...")

model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

print("Model loaded.")


embedding_engine = EmbeddingEngine(
    model=model
)

similarity_engine = SimilarityEngine()


chunks = [
    {
        "title": "Nelson Mandela",
        "content": (
            "Nelson Mandela became South Africa's "
            "first democratically elected president."
        ),
    },
    {
        "title": "Shaka Zulu",
        "content": (
            "Shaka Zulu united many Nguni clans "
            "into the Zulu Kingdom."
        ),
    },
    {
        "title": "Charlotte Maxeke",
        "content": (
            "Charlotte Maxeke was an educator "
            "and political activist."
        ),
    },
]


print("Embedding chunks...")

embedded_chunks = embedding_engine.embed_chunks(
    chunks=chunks
)

print("Chunks embedded.")


query = (
    "Leader imprisoned for 27 years"
)

print(
    f"\nQuery:\n{query}\n"
)

query_embedding = model.encode(
    query,
    convert_to_tensor=True,
)


results = similarity_engine.compare(
    query_embedding=query_embedding,
    embedded_chunks=embedded_chunks,
)


print("\nSemantic Results\n")
print("-" * 60)

for result in results:

    print(result["title"])

    print(
        f"Similarity: "
        f"{result['similarity']:.4f}"
    )

    print()