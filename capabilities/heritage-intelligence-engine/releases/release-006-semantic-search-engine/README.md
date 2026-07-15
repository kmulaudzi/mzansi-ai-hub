# Release 006 — Semantic Search Engine

## Overview

Release 006 transforms the Heritage Intelligence Engine from a keyword-based retrieval system into a semantic search platform.

Previous releases generated embeddings for every heritage document chunk but still relied on keyword matching during retrieval.

This release introduces the **Similarity Engine**, allowing the platform to compare the semantic meaning of a user's question with the semantic meaning of every cached heritage chunk.

Rather than searching for identical words, the Heritage Intelligence Engine now searches for the closest ideas.

---

# Objectives

- Introduce the Similarity Engine.
- Replace keyword retrieval with semantic retrieval.
- Generate embeddings for user queries.
- Compare query embeddings against cached document embeddings.
- Return the most semantically similar heritage knowledge.
- Preserve the existing modular architecture.

---

# New Component

## Similarity Engine

### Responsibility

Compare embeddings using cosine similarity.

Input

```
Query Embedding

+

Embedded Heritage Chunks
```

Output

```
Embedded Heritage Chunks

+

Similarity Score
```

The Similarity Engine performs no learning.

It performs no training.

It performs no prediction.

Its only responsibility is measuring semantic similarity.

---

# Runtime Flow

Application Startup

```
Providers

↓

Documents

↓

Chunking Engine

↓

Embedding Engine

↓

Cached Embedded Chunks
```

User Search

```
User Question

↓

Embedding Engine

↓

Query Embedding

↓

Similarity Engine

↓

Semantic Matches

↓

Ranking

↓

Gradio
```

---

# Semantic Search

Previous releases searched for matching words.

```
User Question

↓

Keyword Search

↓

Matching Documents
```

Release 006 searches for matching meaning.

```
User Question

↓

Embedding

↓

Semantic Similarity

↓

Matching Heritage Knowledge
```

---

# Embedding Engine Evolution

Release 005

```
embed_chunks()
```

Release 006

```
embed_chunks()

embed_text()
```

The Embedding Engine now supports two workflows.

Startup

```
Documents

↓

Embeddings
```

Runtime

```
Question

↓

Embedding
```

---

# Similarity Engine

The Similarity Engine receives

```
Query Embedding

+

Embedded Chunks
```

For every chunk it

- calculates cosine similarity
- enriches the chunk with a similarity score
- sorts results from highest similarity to lowest similarity

The cached knowledge is never modified.

The Similarity Engine works on copies of cached objects.

---

# Architectural Decisions

## Why create a Similarity Engine?

Although sentence-transformers already provides cosine similarity utilities, the Heritage Intelligence Engine requires its own architectural layer.

The Similarity Engine

- hides external AI libraries
- standardises semantic comparison
- preserves architectural consistency
- allows future similarity implementations without changing the application

Future implementations may include

- FAISS
- HNSW
- ChromaDB
- Pinecone
- Milvus

without changing the Retrieval Engine.

---

# Engineering Principles

Release 006 reinforces several architectural principles.

- One engine, one responsibility.
- Business logic remains independent from AI libraries.
- Cached knowledge remains immutable.
- Retrieval Engines orchestrate rather than perform AI.
- Similarity is an independent capability.

---

# What We Built

✅ Similarity Engine

✅ Query embeddings

✅ Semantic retrieval

✅ Cosine similarity

✅ Semantic ranking

✅ Expanded Embedding Engine

---

# Lessons Learned

Semantic search is not a new AI model.

Semantic search is

```
Question

↓

Embedding

↓

Nearest Meaning

↓

Results
```

The Similarity Engine introduced the mathematical foundation that modern Retrieval-Augmented Generation (RAG) systems depend upon.

---

# Current Architecture

```
User

↓

Gradio

↓

Application Engine

↓

Retrieval Engine

↓

Embedding Engine

↓

Similarity Engine

↓

Ranking Engine

↓

Results
```

---

# Next Release

## Release 007 — Vector Database

Release 007 replaces in-memory semantic comparison with a scalable vector index.

Current

```
Query

↓

Compare against every cached vector

↓

Results
```

Next

```
Query

↓

Vector Database

↓

Nearest Neighbours

↓

Results
```

Release 007 prepares the Heritage Intelligence Engine for large-scale knowledge collections.

---

# Project Status

Release 001 ✅ Knowledge Cards

Release 002 ✅ Heritage Search Engine

Release 003 ✅ Document Intelligence

Release 004 ✅ Document Chunking Engine

Release 005 ✅ Embedding Engine

Release 006 ✅ Semantic Search Engine

Release 007 🔜 Vector Database