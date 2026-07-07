# Release 001 — Heritage Knowledge Assistant

## Objective

Build the first capability of Mzansi AI Hub: a Heritage Knowledge Assistant that can answer questions using a Foundation Heritage Dataset and an existing AI language model.

## Release 001 Pipeline

```text
User
  │
  ▼
Question
"Who was Shaka Zulu?"
  │
  ▼
Gradio Interface
  │
  ▼
Heritage Assistant Logic
  │
  ├── Foundation Dataset
  │     └── Heritage knowledge cards
  │
  └── Existing Hugging Face Model
        └── Language understanding and response generation
  │
  ▼
Final Answer
Scope

Included:

Foundation Dataset
Question-answering logic
Gradio interface
GitHub version control

Not included:

Fine-tuning
Embeddings
Vector database
RAG
Image recognition