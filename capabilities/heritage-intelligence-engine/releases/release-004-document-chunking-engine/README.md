# Release 004 — Document Chunking Engine

## Status

✅ Complete

---

# Purpose

Release 004 introduces the Document Chunking Engine into the Heritage Intelligence Engine.

Until Release 003, the platform searched entire documents.

Although functional, treating large documents as a single searchable unit reduces retrieval accuracy because one document may contain many different topics.

Release 004 solves this by introducing a dedicated Chunking Engine that divides documents into smaller searchable units while preserving links back to the original document.

This release prepares the platform for semantic search and Retrieval-Augmented Generation (RAG).

---

# Business Problem

A single heritage document may contain hundreds of pages covering many different subjects.

Searching an entire document often returns results that are too broad.

Instead, the platform should search smaller sections of knowledge.

---

# Architecture Before

```
Providers
    ↓
Documents
    ↓
Search Engine
    ↓
Ranking Engine
```

---

# Architecture After

```
Providers
    ↓
Documents
    ↓
Chunking Engine
    ↓
Chunks
    ↓
Search Engine
    ↓
Ranking Engine
```

---

# New Component

## Chunking Engine

Responsibilities:

- Divide documents into smaller chunks
- Preserve source metadata
- Generate unique Chunk IDs
- Preserve parent document references

The Chunking Engine does **not** search.

The Chunking Engine does **not** rank.

It prepares knowledge for retrieval.

---

# Engineering Principles Introduced

## One Engine, One Responsibility

Chunking is no longer performed by the Retrieval Engine.

A dedicated Chunking Engine owns this responsibility.

---

## Search Smaller Units

The platform now retrieves chunks instead of entire documents.

This improves retrieval precision.

---

## Preserve Traceability

Every chunk remembers:

- Parent document
- Source type
- Source path
- Chunk ID
- Chunk Index

This allows future AI responses to trace answers back to the original heritage document.

---

# Validation

Local Validation

- Chunking Engine compiled
- Retrieval Engine integrated
- Application Engine updated

Colab Validation

- Markdown Provider validated
- PDF Provider validated
- Chunking Engine validated
- Gradio successfully returned chunked search results

---

# Release Outcome

The Heritage Intelligence Engine now searches pieces of knowledge rather than entire documents.

This release lays the architectural foundation for semantic retrieval using embeddings.

---

# Next Release

Release 005 — Embedding Engine

The platform will evolve from keyword search to semantic search by converting chunks into vector representations.