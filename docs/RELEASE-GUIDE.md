# Mzansi AI Hub

# AI Capability Release Guide

Version 1.0

---

# Purpose

This guide defines the standard process for developing and releasing a new AI capability within the Mzansi AI Hub AI Capability Framework.

Every capability follows the same engineering lifecycle to ensure consistency, quality, maintainability, and long-term sustainability.

No capability should skip any stage.

---

# Release Lifecycle

Every capability progresses through the following stages.

```text
Idea
    │
    ▼
Capability Definition
    │
    ▼
README
    │
    ▼
Architecture Review
    │
    ▼
Settings
    │
    ▼
Engine
    │
    ▼
Capability Application
    │
    ▼
Unit Tests
    │
    ▼
Real Model Validation
    │
    ▼
Documentation Review
    │
    ▼
Release Approval
```

---

# Stage 1 — Capability Definition

Clearly identify the capability.

Define:

- Name
- Purpose
- Responsibility
- Inputs
- Outputs
- Future extension points

Ask one question:

> What single problem does this capability solve?

---

# Stage 2 — README

Create the README before writing code.

The README should describe:

- Purpose
- Motivation
- Architecture
- Workflow
- Public interface
- Examples
- Future roadmap

---

# Stage 3 — Architecture Review

Before implementation, confirm:

- Engine responsibility
- Capability Application responsibility
- Layer placement
- Dependencies
- Public interface

Architecture should be reviewed before coding begins.

---

# Stage 4 — Settings

Create `settings.py`.

All configurable values belong here.

Examples include:

- Model names
- Generation parameters
- Thresholds
- Prompt templates
- Default limits

Avoid hard-coded configuration throughout the codebase.

---

# Stage 5 — Engine

Implement the Engine.

The Engine should:

- Solve one problem
- Be reusable
- Be independently testable
- Avoid orchestration
- Avoid presentation logic

---

# Stage 6 — Capability Application

Implement the Capability Application.

Responsibilities include:

- Receiving requests
- Coordinating Engines
- Returning structured results

Applications should remain lightweight.

---

# Stage 7 — Unit Tests

Write comprehensive unit tests.

Unit tests should verify:

- Constructor validation
- Public methods
- Error handling
- Input validation
- Expected outputs

Tests must be:

- Fast
- Repeatable
- Independent

---

# Stage 8 — Real Model Validation

Validate the capability using a real AI model.

Purpose:

- Verify behaviour outside the testing environment
- Confirm integration with production technologies

Validation should demonstrate that the capability performs as intended.

---

# Stage 9 — Documentation Review

Verify that all documentation is complete.

Required documents:

- README
- Public interface
- Examples
- Architecture
- Future improvements

Documentation is considered part of the release.

---

# Stage 10 — Release Approval

A capability is considered complete only when:

- Documentation is complete
- Engine implemented
- Capability Application implemented
- Unit tests pass
- Real model validation succeeds
- Architecture remains compliant

Only then may development begin on the next capability.

---

# Release Checklist

Before declaring a capability complete:

- README completed
- Architecture reviewed
- Settings created
- Engine implemented
- Capability Application implemented
- Unit tests passing
- Real model validation completed
- Documentation updated
- Git committed
- Release tagged

---

# Definition of Done

A capability is complete when it satisfies the AI Capability Standard and successfully passes every stage of the Release Lifecycle.

Completion is determined by engineering quality, not by the amount of code written.

---

# Engineering Principle

> Quality is built into every stage of the release lifecycle.

> A completed capability becomes a permanent building block of the framework.