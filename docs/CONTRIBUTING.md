# Mzansi AI Hub

# Contributing Guide

Version 1.0

---

# Welcome

Thank you for contributing to the Mzansi AI Hub AI Capability Framework.

The purpose of this project is to build reusable AI engineering capabilities that can power multiple intelligence systems.

Examples include:

- Heritage Intelligence
- Telecom Intelligence
- Gaming Intelligence
- Healthcare Intelligence
- Education Intelligence

Before contributing, please read:

- AI-CAPABILITY-STANDARD.md
- ARCHITECTURE.md
- ROADMAP.md

These documents define the engineering philosophy of the project.

---

# Engineering Philosophy

The framework follows one simple rule.

> One Release = One Capability

Every capability must solve one problem well.

Avoid combining multiple responsibilities into a single release.

---

# Development Lifecycle

Every capability follows the same engineering process.

```text
Idea
    │
    ▼
Capability Design
    │
    ▼
README
    │
    ▼
Engine Implementation
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
Release
```

Do not skip any stage.

---

# Standard Capability Structure

Every capability must use the following structure.

```text
release-xxx-capability/

│
├── README.md
├── settings.py
├── <capability>_engine.py
├── <capability>_application.py
├── requirements.txt
│
├── tests/
│
├── docs/
│
└── examples/
```

Maintaining a consistent structure improves maintainability across the framework.

---

# Engine Guidelines

Each Engine must:

- Solve one problem
- Be independently testable
- Be reusable
- Avoid presentation logic
- Avoid orchestration logic

An Engine should never call another Engine directly.

---

# Capability Application Guidelines

Capability Applications coordinate one or more Engines.

Responsibilities include:

- Input validation
- Workflow orchestration
- Returning structured results

Applications should never contain AI algorithms.

---

# Testing Requirements

Every capability must include:

## Unit Tests

- Fast
- Independent
- Repeatable
- No external services

## Real Model Validation

Demonstrate the capability using an actual AI model.

The validation script should verify that the capability behaves correctly outside of the unit test environment.

---

# Documentation Requirements

Every capability must include:

- README
- Purpose
- Architecture
- Public Interface
- Examples
- Future Extension Points

Documentation is considered part of the implementation.

---

# Coding Standards

Use:

- Descriptive names
- Type hints where appropriate
- Docstrings for public classes and methods
- Small, focused methods
- Single Responsibility Principle

Avoid:

- Hidden side effects
- Large functions
- Tight coupling
- Duplicate logic

---

# Pull Request Checklist

Before submitting a contribution, verify:

- Capability follows the AI Capability Standard.
- Architecture remains unchanged.
- Unit tests pass.
- Real model validation succeeds.
- Documentation has been updated.
- Public interfaces remain stable.

---

# Vision

This framework is designed to evolve over many years.

Every contribution should improve:

- Reusability
- Maintainability
- Readability
- Testability
- Extensibility

---

# Engineering Principle

> Build capabilities that future engineers will understand without explanation.