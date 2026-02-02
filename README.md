# Multi-Agent-RAG-Validator
Multi-Agent RAG Validator is a research-oriented Retrieval-Augmented Generation (RAG) system designed to validate user queries against uploaded documents using a modular, agent-based architecture. The system ensures responses are grounded, explainable, and source-backed, making it suitable for academic and analytical use cases.

## Core Objectives

- Prevent hallucinated responses from LLMs
- Ensure answers are strictly derived from provided documents
- Provide transparent source attribution
- Support multiple document formats in a unified pipeline
- Maintain production-safe, deterministic behavior where possible

---

## Supported Document Types

The system currently supports ingestion and retrieval from:

- PDF (`.pdf`)
- Word documents (`.docx`)
- PowerPoint presentations (`.pptx`)
- Excel files (`.xlsx`)
- Plain text files (`.txt`)

Each document type is handled by a dedicated ingestion module optimized for that format.

---

## High-Level System Architecture

The system consists of five major layers:

1. User Interface Layer
2. Document Ingestion Layer
3. Embedding & Vector Store Layer
4. Agentic Orchestration Layer
5. Response Generation Layer

All components are loosely coupled to allow independent testing and upgrades.

---

## Detailed Workflow

### 1. File Upload & Storage

- Users upload documents via the Streamlit UI
- Files are automatically routed into subfolders (`pdf/`, `docx/`, `pptx/`, `xlsx/`, `texts/`) based on file extension
- This folder-based segregation simplifies ingestion and debugging

---

### 2. Ingestion Pipeline

Each document type has a dedicated ingestor:

#### PDF Ingestor
- Extracts text page-by-page
- Preserves page numbers as metadata

#### DOCX Ingestor
- Extracts full document text
- Useful for resumes, reports, and profiles

#### PPTX Ingestor
- Extracts text slide-by-slide
- Maintains slide numbers for traceability

#### Excel Ingestor
- Reads all sheets in a workbook
- Converts tabular data into structured text
- Preserves sheet names as metadata

#### Text Ingestor
- Reads raw text files directly

All ingestors output a standardized `Document` object containing:

- `page_content`
- `metadata` (document type, source file, section/page/slide)

---

### 3. Text Chunking

- Extracted documents are split into smaller overlapping chunks
- Chunking is done using a recursive strategy
- Overlap ensures semantic continuity across chunks

This improves retrieval accuracy during similarity search.

---

### 4. Embedding Generation

- Each text chunk is converted into a vector embedding
- Embeddings are generated using OpenAI Embeddings
- Embeddings capture semantic meaning rather than keyword matching

This step happens only once during ingestion or index rebuild.

---

### 5. Vector Storage (FAISS)

- All embeddings are stored in a FAISS vector index
- FAISS enables fast similarity search using dense vectors
- Index is persisted locally for reuse

---

## Agentic Orchestration Layer

The system uses multiple agents coordinated through an orchestrator.

---

### Query Understanding Agent

- Classifies the user query into categories such as:
  - `research`
  - `conceptual`
  - `data`
  - `profile`
  - `presentation`

This classification influences downstream routing.

---

### Document Routing Agent

- Deterministically selects which document types should be searched
- Uses rule-based logic (no LLM)
- Ensures only relevant document categories are queried

Even though it does not use an LLM, it is called an agent because it:

- Has a clear decision-making role
- Operates independently
- Can be replaced or upgraded later

---

### Retrieval Agent

- Performs similarity search on the FAISS index
- Applies document-type filters provided by the routing agent
- Returns the most relevant chunks with metadata

---

### Fact Check Agent

- Evaluates whether retrieved evidence supports the user query
- Produces a structured verdict (e.g., `SUPPORTED`, `CONTRADICTED`, `UNKNOWN`)
- Adds reasoning used for final response generation

---

### Response Composition Agent

- Uses an LLM to generate the final answer
- Strictly constrained to retrieved evidence
- Produces:
  - Clear verdict
  - Natural-language explanation
  - Confidence note
  - Exact source citations

This agent is heavily prompt-guarded to prevent hallucination.

---

## Context Construction Strategy

- Only retrieved chunks are passed to the LLM
- Metadata is preserved throughout the pipeline
- No external knowledge is injected
- Sources are cited exactly as stored

This guarantees transparency and traceability.

---

## Technology Stack

### Language
- Python

### Frameworks & Libraries
- LangChain
- LangChain Community
- Streamlit
- FAISS
- OpenAI SDK
- Pandas
- PyPDF
- python-pptx
- python-dotenv

---

## Project Structure

```text
Multi-Agent-RAG-Validator/
│
├── agents/               # Query, routing, retrieval, fact-check agents
├── ingestion/            # Document ingestion logic
├── orchestration/        # Agent orchestration and pipelines
├── vectorstore/          # FAISS storage and loading
├── ui/                   # Streamlit interface
├── utils/                # Logging and helpers
├── data/                 # Uploaded documents
├── tests/                # Component-level tests
│
├── main.py               # Application entry point
├── requirements.txt
└── README.md
```



## Design Decisions

- Rule-based routing for reliability
- LLM usage restricted to reasoning and language generation
- Explicit metadata propagation
- Separate ingestion per document type
- Test-first approach for ingestion and retrieval

---

## Limitations

- Performance depends on document text quality
- Excel and PPT retrieval effectiveness depends on textual richness
- Not designed for real-time streaming ingestion
- Local FAISS index limits horizontal scalability
