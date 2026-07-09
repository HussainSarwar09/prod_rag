# Production RAG

A production-grade **Retrieval-Augmented Generation (RAG)** application built with **Python**, **FastAPI**, and **LangGraph** using an enterprise software architecture.

The goal of this project is not simply to build a chatbot, but to demonstrate how a modern AI application should be designed, tested, deployed, and maintained in production.

---

# Objectives

* Build a production-quality RAG application
* Use LangGraph for orchestration
* Follow clean architecture principles
* Implement automated testing and CI/CD
* Support enterprise-ready extensibility
* Serve as a portfolio-quality AI Engineering project

---

# Technology Stack

| Component            | Technology        |
| -------------------- | ----------------- |
| Language             | Python 3.13       |
| API                  | FastAPI           |
| Orchestration        | LangGraph         |
| Package Manager      | Poetry            |
| Configuration        | Pydantic Settings |
| Logging              | Loguru            |
| Testing              | Pytest            |
| Linting & Formatting | Ruff              |
| Containers           | Docker            |
| CI/CD                | GitHub Actions    |

---

# Current Status

**Sprint 1 – Project Foundation**

Completed:

* Project structure
* Dependency management with Poetry
* FastAPI application
* Application Factory pattern
* Centralized configuration
* API versioning
* Structured logging
* Docker support
* Unit testing framework
* GitHub Actions
* Pre-commit hooks

---

# Project Structure

```text
prod-rag/
│
├── app/
│   ├── api/
│   ├── config/
│   ├── core/
│   ├── graphs/
│   ├── ingestion/
│   ├── chunking/
│   ├── embeddings/
│   ├── retrieval/
│   ├── reranker/
│   ├── llm/
│   ├── services/
│   ├── schemas/
│   └── utils/
│
├── tests/
├── docker/
├── docs/
├── scripts/
├── data/
├── chroma/
│
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

# Getting Started

## Clone the Repository

```bash
git clone <repository-url>

cd prod-rag
```

## Install Dependencies

```bash
poetry install
```

## Activate the Environment

```bash
poetry shell
```

or

```bash
poetry run <command>
```

---

# Run the Application

```bash
poetry run uvicorn app.main:app --reload
```

Open:

* http://127.0.0.1:8000/
* http://127.0.0.1:8000/docs
* http://127.0.0.1:8000/api/v1/health

---

# Docker

Build:

```bash
docker compose -f docker/docker-compose.yml build
```

Run:

```bash
docker compose -f docker/docker-compose.yml up
```

---

# Testing

Run all tests:

```bash
poetry run pytest
```

Run unit tests:

```bash
poetry run pytest -m unit
```

Run integration tests:

```bash
poetry run pytest -m integration
```

Run end-to-end tests:

```bash
poetry run pytest -m e2e
```

---

# Code Quality

Run Ruff:

```bash
poetry run ruff check .
```

Format code:

```bash
poetry run ruff format .
```

Run MyPy:

```bash
poetry run mypy app
```

---

# CI/CD

Every push and pull request automatically executes:

* Ruff
* MyPy
* Pytest
* Coverage generation

---

# Roadmap

## Sprint 1

* Project foundation
* Docker
* Testing
* CI/CD

## Sprint 2

* Document ingestion
* LangGraph ingestion graph

## Sprint 3

* Chunking pipeline

## Sprint 4

* Embedding generation

## Sprint 5

* ChromaDB integration

## Sprint 6

* Retrieval pipeline

## Sprint 7

* LLM integration

## Sprint 8

* Citation support

## Sprint 9

* Hybrid retrieval

## Sprint 10

* Cross-encoder reranking

## Sprint 11

* Automated evaluation

## Sprint 12

* Production-ready RAG v1.0.0

---

# License

This project is intended for educational and portfolio purposes. A production-ready open-source license will be selected before the v1.0.0 release.
