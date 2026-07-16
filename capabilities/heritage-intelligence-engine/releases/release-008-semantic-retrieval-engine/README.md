# Release 007 — Vector Database Engine

## Overview

Release 007 introduces the **Vector Database Engine** into the Heritage Intelligence Engine.

Previous releases generated embeddings and compared them directly using semantic similarity.

That approach works for small datasets, but it becomes inefficient as the number of heritage chunks grows.

Release 007 solves this by storing embedded heritage chunks inside a searchable FAISS vector index.

The platform can now retrieve nearest-neighbour chunks through a stable vector database contract.

---

# Objectives

- Introduce the Vector Database Engine.
- Build a searchable vector index.
- Store embedded chunks and preserve their metadata.
- Retrieve nearest neighbours using FAISS.
- Replace direct similarity scanning with indexed retrieval.
- Keep FAISS hidden behind the platform’s own architectural contract.
- Validate the Vector Database Engine independently before full application integration.

---

# New Component

## Vector Database Engine

**Python file**

```text
vector_database_engine.py
```

**Responsibility**

Build and search a vector index.

**Public contract**

```python
build_index(embedded_chunks)
search(query_embedding, top_k)
```

**Receives**

```text
Embedded heritage chunks
Query embedding
```

**Stores**

```text
FAISS vector index
Embedded chunk metadata
```

**Returns**

```text
Nearest-neighbour chunks
Similarity scores
Vector index positions
```

The Vector Database Engine does not:

- load documents
- create chunks
- generate embeddings
- validate user queries
- create the user interface

---

# Architecture Before

```text
User Query
    ↓
Embedding Engine
    ↓
Similarity Engine
    ↓
Compare against cached vectors
    ↓
Semantic Results
```

---

# Architecture After

```text
User Query
    ↓
Embedding Engine
    ↓
Vector Database Engine
    ↓
FAISS Vector Index
    ↓
Nearest-Neighbour Results
```

---

# Application Startup

```text
Provider Layer
providers/markdown_provider.py
providers/pdf_provider.py
    ↓
Documents
    ↓
Chunking Engine
chunking_engine.py
    ↓
Chunks
    ↓
Embedding Engine
embedding_engine.py
    ↓
Embedded Chunks
    ↓
Vector Database Engine
vector_database_engine.py
    ↓
FAISS Vector Index
```

This workflow runs once during application startup.

---

# Search-Time Flow

```text
User Question
    ↓
Gradio Interface
app.py
    ↓
Application Engine
application_engine.py
    ↓
Retrieval Engine
retrieval_engine.py
    ↓
Embedding Engine
embedding_engine.py
    ↓
Query Embedding
    ↓
Vector Database Engine
vector_database_engine.py
    ↓
Nearest Heritage Chunks
    ↓
Formatted Results
```

---

# FAISS Integration

Release 007 uses:

```text
faiss-cpu
```

The Python import is:

```python
import faiss
```

The initial implementation uses:

```text
IndexFlatIP
```

The vectors are normalized before they are added to the index.

With normalized vectors, inner-product search behaves like cosine similarity.

This provides exact nearest-neighbour retrieval while preserving the engine contract for future index implementations.

---

# Vector-to-Metadata Mapping

FAISS stores vectors by numeric position.

The Vector Database Engine separately stores the original embedded chunks.

```text
FAISS vector position 0
    ↔
embedded_chunks[0]

FAISS vector position 1
    ↔
embedded_chunks[1]
```

When FAISS returns a vector position, the engine uses that position to retrieve the corresponding heritage chunk and metadata.

The returned object is enriched with:

```text
similarity
vector_index
```

---

# Architectural Decisions

## Why not call it `FaissEngine`?

FAISS is an implementation detail.

The architecture depends on:

```text
VectorDatabaseEngine
```

not on:

```text
FAISS
```

This allows future implementations such as:

- Qdrant
- Milvus
- Pinecone
- Weaviate
- Chroma
- another FAISS index

without changing the rest of the Heritage Intelligence Engine.

---

## Why `build_index()` instead of `store()`?

`build_index()` clearly communicates that the vectors are being organized into a searchable structure.

The engine does more than save vectors.

It prepares them for efficient retrieval.

---

## Why store embedded chunks as well as vectors?

Vectors alone have no human-readable context.

The embedded chunk preserves:

- title
- content
- source type
- filename
- chunk ID
- parent document
- embedding metadata

This allows the platform to reconnect machine-readable semantic memory with human-readable heritage knowledge.

---

# Engine Validation

The Vector Database Engine was validated independently before full platform integration.

Validation flow:

```text
Sample Heritage Chunks
    ↓
Embedding Engine
    ↓
Vector Database Engine.build_index()
    ↓
User Query
    ↓
Embedding Engine.embed_text()
    ↓
Vector Database Engine.search()
    ↓
Nearest Neighbours
```

Successful validation confirmed that a semantic query such as:

```text
Leader imprisoned for 27 years
```

retrieved the Nelson Mandela chunk as the nearest result.

---

# Engineering Principles Reinforced

- One engine, one responsibility.
- Design the contract before choosing the technology.
- External technologies remain behind internal contracts.
- Build expensive indexes once and reuse them.
- Validate every engine independently before platform integration.
- Preserve metadata alongside machine-readable vectors.
- Architectures should outlive technologies.

---

# What We Built

✅ Vector Database Engine

✅ FAISS index construction

✅ Indexed semantic memory

✅ Nearest-neighbour retrieval

✅ Vector-to-chunk metadata mapping

✅ CPU-compatible Colab implementation

✅ Stable `build_index()` and `search()` contracts

---

# Current Limitation

The current FAISS implementation uses an exact flat index.

It is suitable for the current proof of concept and provides a clean architectural foundation.

Future versions may introduce:

- approximate nearest-neighbour indexes
- persistent vector storage
- metadata filtering
- index saving and loading
- incremental document updates
- hybrid keyword and vector retrieval

---

# Release Outcome

The Heritage Intelligence Engine now has an indexed semantic memory layer.

It no longer needs to perform direct similarity comparison across the application.

Instead, it asks the Vector Database Engine for the nearest heritage knowledge.

---

# Next Release

## Release 008 — Semantic Retrieval Engine

Release 008 will improve the quality of retrieved knowledge.

The Vector Database Engine finds nearest-neighbour candidates.

The Retrieval Engine will decide which candidates are strong enough and useful enough to continue through the pipeline.

Planned capabilities include:

- similarity thresholds
- retrieval limits
- metadata filtering
- duplicate reduction
- stronger retrieval contracts
- preparation for grounded answer generation

---

# Project Status

| Release | Capability | Status |
|---|---|---|
| 001 | Knowledge Cards | ✅ Complete |
| 002 | Heritage Search Engine | ✅ Complete |
| 003 | Document Intelligence | ✅ Complete |
| 004 | Document Chunking Engine | ✅ Complete |
| 005 | Embedding Engine | ✅ Complete |
| 006 | Semantic Search Engine | ✅ Complete |
| 007 | Vector Database Engine | ✅ Complete |
| 008 | Semantic Retrieval Engine | 🔄 Next |