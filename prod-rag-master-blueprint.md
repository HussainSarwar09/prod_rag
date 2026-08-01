# prod-rag --- Master Blueprint

> Canonical design document for the project. This file is intended to be
> reused in any future conversation regardless of the current sprint.

# Vision

Build a production-grade Retrieval-Augmented Generation (RAG) platform
using:

-   Python 3.13
-   FastAPI
-   LangGraph (from day one)
-   Poetry
-   Docker
-   Clean Architecture
-   SOLID principles
-   Dependency Inversion
-   OSS-first stack

The project will evolve from a production-quality RAG application into a
modular enterprise RAG platform.

# Core Technology Stack

-   FastAPI
-   LangGraph
-   LangChain Core
-   Pydantic Settings
-   Loguru
-   Ruff
-   MyPy
-   Pytest
-   Docker
-   GitHub Actions

Planned providers:

-   Ollama
-   BGE Embeddings
-   Chroma
-   BM25
-   Cross Encoder
-   RAGAS

# Architectural Principles

-   LangGraph-first orchestration
-   Versioned REST APIs
-   Application Factory
-   Clean Architecture
-   Domain-driven organization
-   Dependency Inversion
-   Protocol-based interfaces
-   Providers encapsulate third-party libraries
-   Business logic never depends directly on infrastructure

# Logical Architecture

``` text
Clients
   │
FastAPI
   │
API
   │
Graphs (LangGraph)
   │
Services
   │
Domain
   │
Core Infrastructure
   ├── Interfaces
   ├── Factories
   ├── Providers
   └── Container
```

# Layer Responsibilities

  Layer        Responsibility
  ------------ --------------------------
  api          HTTP endpoints
  graphs       LangGraph orchestration
  services     Business logic
  domain       Business entities
  schemas      API DTOs
  config       Configuration
  core         Infrastructure
  interfaces   Contracts
  providers    Concrete implementations

# Non-negotiable Conventions

-   Use `graphs/`, never `workflows/`
-   Domain models use dataclasses
-   API models belong in `schemas`
-   Use `typing.Protocol`
-   Ruff replaces Black
-   Command Prompt commands in documentation
-   Docker-first development
-   Every sprint ends with tests, docs, CI, and a Git tag

# Sprint Roadmap

1.  Foundation
2.  Document Ingestion
3.  Chunking
4.  Embeddings
5.  Vector Database
6.  Retrieval
7.  LLM Integration
8.  Citations
9.  Hybrid Retrieval
10. Reranking
11. Evaluation
12. Production Platform v1.0.0

# Continuation Instructions

When starting a new conversation:

1.  Use this blueprint as the architectural reference.
2.  Tell ChatGPT which sprint to continue.
3.  Preserve all architectural decisions.
4.  Avoid structural refactoring unless technically necessary.
5.  Continue using:
    -   File location
    -   CMD commands
    -   Full file contents
    -   Purpose
    -   Architecture explanation

This file intentionally omits sprint-specific implementation details.
