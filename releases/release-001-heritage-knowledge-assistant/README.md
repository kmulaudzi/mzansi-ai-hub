# Release 001 – Heritage Knowledge Assistant (Architecture Validation Prototype)

## Vision

This project marks the beginning of the **Heritage Intelligence Platform**.

Rather than building a standalone chatbot, the long-term goal is to develop a reusable AI platform capable of understanding, retrieving, and generating knowledge from trusted South African heritage sources.

The Heritage Knowledge Assistant is the first capability built on this platform.

---

# Objective

Validate the overall architecture required for a Heritage Intelligence Platform by building a simple end-to-end AI assistant.

The focus of this release was not perfect answers, but validating the interaction between:

- Knowledge
- Retrieval
- Prompting
- AI Generation
- User Interface

---

# Capabilities Delivered

This release introduces the following capabilities:

✅ Knowledge Card Loader

- Loads structured Markdown knowledge cards
- Creates an internal knowledge base

---

✅ Simple Retrieval

- Searches knowledge cards using keyword matching
- Returns the best matching card

---

✅ Prompt Builder

- Combines retrieved knowledge with the user's question
- Sends structured prompts to the language model

---

✅ AI Response Generation

- Uses Google's FLAN-T5 model
- Generates natural language answers

---

✅ Gradio User Interface

- Web interface for interacting with the assistant
- Demonstrates the complete AI workflow

---

# Project Structure

```
release-001-heritage-knowledge-assistant/

foundation-dataset/
    knowledge-cards/

knowledge_loader.py

heritage_search.py

prompt_builder.py

ai_response_generator.py

app.py
```

---

# What We Learned

This release achieved its primary objective by validating the architecture while also revealing important limitations.

## 1. Keyword Search Does Not Scale

Simple keyword matching performs poorly as the knowledge base grows.

Example:

Question:

"What is Mapungubwe?"

Incorrect Retrieval:

"Ndebele Art"

This demonstrated the need for semantic retrieval.

---

## 2. Large Language Models Already Have Prior Knowledge

FLAN-T5 sometimes ignored retrieved context and answered from its own pre-trained knowledge.

This highlighted the importance of stronger prompt engineering and improved retrieval.

---

## 3. Better Models Alone Do Not Solve Retrieval Problems

Changing the language model does not improve retrieval quality.

Knowledge retrieval must improve first.

---

## 4. Architecture Matters More Than Individual Models

This project confirmed that separating:

- Knowledge
- Retrieval
- Prompting
- Generation

creates a reusable architecture that can evolve independently.

---

# Why This Release Matters

This release is considered an **Architecture Validation Prototype**.

Its purpose was to validate the platform architecture and identify the capabilities required for future releases.

The lessons learned directly influence the design of Release 002.

---

# Next Capability

## Capability 002 — Document Intelligence

The next release introduces the platform's first reusable enterprise capability.

New capabilities include:

- Universal Document Loader
- TXT support
- Markdown support
- PDF support
- Word support
- PowerPoint support
- Document Parsing
- Cleaner text extraction
- Preparation for Chunking
- Preparation for Embeddings

This moves the platform away from manually created knowledge cards toward real heritage documents.

---

# Long-Term Vision

The Heritage Knowledge Assistant is only the first application built on the platform.

Future applications include:

- Heritage Research Assistant
- Education Assistant
- Museum Assistant
- Tourism Assistant
- Heritage Gaming AI
- Developer APIs

All applications will reuse the same platform capabilities.

---

# Engineering Principles

This project follows a capability-driven architecture.

Every release introduces reusable platform capabilities rather than isolated features.

Core principles:

- Business before Technology
- Architecture before Models
- Capabilities before Features
- Knowledge before Generation
- Experiment in the Laboratory
- Engineer for Production

---

# Status

✅ Release 001 Complete

Architecture successfully validated.

Ready to begin Capability 002 – Document Intelligence.

---

Built as part of the TIC-IT Artificial Intelligence Strategy.

The long-term objective is to create a reusable Heritage Intelligence Platform capable of supporting education, research, tourism, museums, gaming, and future AI applications using trusted South African heritage knowledge.