Great. Next, we define the capability boundaries before touching Python.

## Step 9 — Create the architecture document

Run:

```bash
touch docs/architecture.md
```

Then open it:

```bash
code docs/architecture.md
```

Paste this:

````markdown
# Release 011 Architecture

## Capability

Evidence Retrieval

## Purpose

The capability receives a user question and returns ranked heritage evidence.

It does not generate the final answer.

## Input

```python
question: str
````

## Output

```python
{
    "success": True,
    "capability": "Evidence Retrieval",
    "release": "011",
    "question": "...",
    "evidence": [
        {
            "title": "...",
            "content": "...",
            "score": 0.0,
            "source": "..."
        }
    ]
}
```

## Engine Responsibility

The Evidence Retrieval Engine may:

* accept a question
* request evidence from an existing retrieval component
* validate retrieved results
* standardise evidence into one output format
* limit the number of returned results

The engine must not:

* generate an answer
* summarise evidence
* modify the original evidence content
* interact with Gradio
* contain presentation logic

## Application Responsibility

The Evidence Retrieval Application may:

* validate the user question
* call the Evidence Retrieval Engine
* return the public capability response
* handle controlled errors

The application must not:

* perform retrieval directly
* rank evidence directly
* generate an answer
* contain model logic

## Flow

```text
User Question
      |
      v
EvidenceRetrievalApplication
      |
      v
EvidenceRetrievalEngine
      |
      v
Existing Retrieval Component
      |
      v
Ranked Evidence
      |
      v
Structured Capability Response
```

## Dependency Rule

Release 011 must reuse an existing retrieval capability.

It must not rebuild keyword search, semantic search, ranking, embeddings, or vector storage.

## Completion Criteria

Release 011 is complete when it can:

* accept a valid question
* retrieve ranked evidence
* return evidence in a stable structure
* handle empty questions safely
* handle no-result cases safely
* pass unit tests

````

Save it, then run:

```bash
ls docs
````

Expected output:

```text
architecture.md
```

Stop there and send me the result.
