# Sprint Breakdown

Detailed sprint split for the Production RAG project, from Sprint 0/1 through the final production platform release.

## Sprint 0 / Sprint 1: Foundation

Purpose:
Establish the project skeleton, engineering standards, and delivery workflow for all future sprints.

Activities:
- Create the base project structure under `app/`, `tests/`, `docs/`, `scripts/`, and `docker/`
- Set up Poetry for dependency management
- Configure FastAPI application bootstrap
- Add LangGraph project scaffolding
- Establish Clean Architecture and domain-driven folder layout
- Add application settings with Pydantic Settings
- Add centralized logging setup
- Configure Ruff, MyPy, and Pytest
- Create Docker and Docker Compose foundations
- Set up GitHub Actions for linting, typing, and test automation
- Add basic health endpoints
- Establish coding conventions and repository documentation

Modules / functionality:
- `app/main.py`
- `app/config/`
- `app/core/`
- `app/api/`
- `tests/`
- `docker/`
- `.github/workflows/`

Exit criteria:
- App starts successfully
- Health endpoints respond
- CI passes
- Linting, typing, and test tooling are in place

## Sprint 2: Document Ingestion

Purpose:
Build the pipeline for reading and normalizing source documents into internal domain objects.

Activities:
- Implement document readers for text and PDF
- Implement document loaders for `.txt`, `.md`, and `.pdf`
- Add file type detection and loader selection
- Normalize raw file contents into `Document` domain entities
- Extract metadata such as filename, extension, MIME type, checksum, and page count
- Add ingestion-related exceptions and error handling
- Add loader factory wiring in the container
- Add unit tests for readers, loaders, and metadata extraction

Modules / functionality:
- `app/readers/`
- `app/loaders/`
- `app/services/metadata/`
- `app/domain/document.py`
- `app/domain/document_metadata.py`
- `app/exceptions/`

Exit criteria:
- Supported file types can be loaded into normalized `Document` objects
- Metadata extraction is reliable
- Reader and loader tests pass

## Sprint 3: Chunking

Purpose:
Split normalized documents into retrieval-ready chunks with stable source traceability.

Activities:
- Implement deterministic token-window chunking
- Preserve source spans and character offsets
- Generate stable chunk IDs
- Link neighboring chunks
- Propagate document metadata into chunk metadata
- Add Markdown-aware heading and section provenance
- Add chunk validation rules
- Add chunking settings and dependency-container wiring
- Add unit tests for chunk boundaries, overlap, IDs, provenance, and edge cases

Modules / functionality:
- `app/chunking/`
- `app/domain/chunk.py`
- `app/domain/chunk_metadata.py`
- `app/core/interfaces/chunker.py`
- `app/config/chunking.py`

Exit criteria:
- Chunking works reliably for supported source types
- Chunks preserve traceability for downstream citations and debugging
- Chunking configuration and tests are in place

## Sprint 3.5: Enterprise Chunking Strategy Layer

Purpose:
Extend baseline chunking into a more production-shaped, strategy-driven chunking pipeline.

Activities:
- Add multiple chunking strategies
- Implement config-driven file-type chunking policies
- Support automatic strategy selection by extension and MIME type
- Add code-aware, JSON-aware, sentence-based, paragraph-based, and Markdown-aware chunking
- Add chunk-level metadata identifying the strategy used
- Add tests for strategy selection, file-type policy overrides, and fallback behavior

Modules / functionality:
- `app/chunking/chunker.py`
- `app/config/chunking.py`
- `tests/unit/chunking/test_chunker.py`

Exit criteria:
- Different chunking strategies can be selected by config or policy
- File-type-aware chunking behavior is implemented
- Strategy metadata is preserved per chunk

## Sprint 4: Embeddings

Purpose:
Generate embeddings for chunks using configurable local-first or remote providers.

Activities:
- Define a stable embedding provider interface
- Implement a local BGE embedding provider
- Add support for an optional remote provider such as OpenAI embeddings
- Create provider-aware embedding configuration
- Add deterministic mock provider for tests
- Add batching support for embedding generation
- Integrate embedding creation into the ingestion service
- Extend chunks to carry embedding vectors in memory
- Add unit tests for provider selection and ingestion embedding flow
- Prepare the ground for tokenizer-aware chunk budgeting

Modules / functionality:
- `app/core/interfaces/embedding.py`
- `app/core/providers/embeddings/`
- `app/config/embedding.py`
- `app/services/ingestion/service.py`
- `app/domain/chunk.py`
- `app/core/container.py`

Exit criteria:
- Chunks can be embedded through a configurable provider
- Local-first provider path works architecturally
- Tests cover provider selection and embedding attachment flow

## Sprint 5: Vector Database

Purpose:
Persist embedded chunks in a vector database and support safe re-ingestion workflows.

Activities:
- Implement the vector store provider interface
- Build the Chroma provider
- Persist chunk text, vectors, IDs, and metadata into the vector store
- Add collection configuration and wiring
- Implement idempotent upsert behavior by stable chunk ID
- Support re-ingestion without duplicate vectors
- Add stale chunk cleanup for changed documents
- Add vector store integration tests
- Add document-level indexing and re-indexing flow

Modules / functionality:
- `app/core/interfaces/vectorstore.py`
- `app/core/providers/vectorstores/chroma.py`
- `app/config/vectorstore.py`
- `app/services/ingestion/service.py`
- `app/core/container.py`

Exit criteria:
- Embedded chunks persist in Chroma
- Re-ingesting the same document does not duplicate entries
- Vector store integration tests pass

## Sprint 6: Retrieval

Purpose:
Retrieve the most relevant chunks for a user query.

Activities:
- Implement query embedding generation
- Add similarity search against the vector database
- Define retrieval service contracts
- Add configurable `top_k`
- Normalize retrieval response objects
- Add retrieval APIs and service wiring
- Add retrieval tests and baseline relevance checks

Modules / functionality:
- `app/retrieval/`
- `app/services/retrieval/`
- `app/domain/query.py`
- `app/api/v1/retrieval.py`

Exit criteria:
- Query text can retrieve relevant chunks from the vector store
- Retrieval API returns ranked chunk results

## Sprint 7: LLM Integration

Purpose:
Connect retrieval with generation to produce grounded answers.

Activities:
- Define LLM provider interface
- Implement local-first LLM provider such as Ollama
- Build prompt assembly from retrieved context
- Add answer generation service
- Wire LangGraph nodes for retrieval and generation
- Add configurable temperature and token controls
- Add basic answer API endpoint
- Add unit tests for prompt composition and generation orchestration

Modules / functionality:
- `app/core/interfaces/llm.py`
- `app/core/providers/llms/`
- `app/graphs/`
- `app/prompts/`
- `app/services/chat/`
- `app/api/v1/chat.py`

Exit criteria:
- Retrieved context is passed to the LLM
- Grounded answer generation works end to end

## Sprint 8: Citations

Purpose:
Make generated answers traceable back to source chunks and documents.

Activities:
- Add citation models and response schema support
- Return source chunk metadata with answers
- Map answer context to chunk offsets, pages, and headings
- Support citation-ready output in the API layer
- Add tests for source traceability and citation formatting

Modules / functionality:
- `app/domain/citation.py`
- `app/schemas/`
- `app/services/chat/`
- `app/api/v1/chat.py`

Exit criteria:
- Answers include reliable source attribution
- Citations map back to chunk metadata and document provenance

## Sprint 9: Hybrid Retrieval

Purpose:
Improve recall by combining dense and lexical retrieval.

Activities:
- Add BM25 or equivalent sparse retrieval support
- Build hybrid retrieval orchestration
- Merge and normalize dense and sparse scores
- Add configuration for retrieval mode selection
- Add tests for dense-only, sparse-only, and hybrid retrieval

Modules / functionality:
- `app/retrieval/`
- `app/services/retrieval/`
- `app/config/`

Exit criteria:
- Hybrid retrieval can be enabled through config
- Combined retrieval outperforms baseline recall on target scenarios

## Sprint 10: Reranking

Purpose:
Improve precision by reranking initially retrieved chunks.

Activities:
- Define reranker provider interface
- Add cross-encoder or reranker provider implementation
- Rerank retrieved candidate chunks before generation
- Add configurable reranking thresholds and cutoffs
- Add tests for ranking behavior and provider wiring

Modules / functionality:
- `app/core/interfaces/reranker.py`
- `app/core/providers/rerankers/`
- `app/services/retrieval/`

Exit criteria:
- Retrieved results are reranked before final context selection
- Reranker provider can be swapped through config

## Sprint 11: Evaluation

Purpose:
Measure retrieval and answer quality systematically.

Activities:
- Add evaluation dataset handling
- Implement retrieval and generation quality metrics
- Add RAGAS or equivalent evaluation hooks
- Track experiment runs and outputs
- Add admin or evaluation endpoints if needed
- Build repeatable evaluation scripts

Modules / functionality:
- `app/evaluation/`
- `app/services/evaluation/`
- `app/api/v1/evaluation.py`
- `scripts/`

Exit criteria:
- Evaluation can be run repeatedly on fixed datasets
- Retrieval and answer quality metrics are visible

## Sprint 12: Production Platform v1.0.0

Purpose:
Harden the system into a production-ready modular RAG platform.

Activities:
- Complete operational hardening
- Add observability, structured logging, and health diagnostics
- Improve configuration ergonomics and secret handling
- Add deployment-ready Docker configuration
- Review security, dependency, and failure-handling posture
- Finalize CI/CD and release automation
- Add production documentation and runbooks
- Prepare versioned release tag and release notes

Modules / functionality:
- Cross-cutting updates across `app/`, `docker/`, `docs/`, `scripts/`, and CI

Exit criteria:
- End-to-end pipeline is stable and documented
- Operational checks and release process are in place
- System is ready for a `v1.0.0` milestone release
