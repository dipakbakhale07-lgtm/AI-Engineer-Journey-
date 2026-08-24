# Day 5 — Prepare Documents for RAG

## Day Focus

Today I worked on the document-preparation stage of Project 1 — RAG Knowledge Assistant.

The goal was to understand how source documents become searchable pieces before building the actual RAG pipeline.

---

## What I Learned Today

The RAG system should not simply send an entire document to the LLM for every question.

Instead, documents are prepared so that relevant information can later be retrieved efficiently.

Basic preparation flow:

Documents
↓
Cleaning
↓
Chunking
↓
Metadata
↓
Embeddings
↓
Vector Store
↓
Retrieval

---

## Document Set

I prepared three source documents for the first knowledge base:

- ai-fundamentals.md
- llm-generative-ai.md
- rag-fundamentals.md

The documents were written as Markdown knowledge material focused on AI, LLM/Generative AI, and RAG concepts.

I chose three relevant documents instead of adding empty or unnecessary files.

---

## Document Cleaning

The source documents were checked for obvious issues such as:

- Duplicate content
- Irrelevant content
- Broken text
- Unnecessary material
- Private information
- Secrets or API keys

The goal was to keep the source knowledge clean before chunking.

---

## Chunking

Chunking means dividing a document into smaller pieces called chunks.

The goal is to create retrieval units that contain enough information to preserve meaning without including unnecessary content.

The main trade-off is:

Too small
↓
Important context can be lost

Too large
↓
Too much unrelated information can be included

Therefore, chunking should be tested rather than chosen blindly.

---

## Section-Based Chunking Experiment

The first experiment used Markdown `##` headings as natural boundaries.

The three documents were analyzed using section-based chunking.

Observed results:

- ai-fundamentals.md: 6 sections
- llm-generative-ai.md: 7 sections
- rag-fundamentals.md: 22 sections

A problem was found with the top-level `#` document title.

The title-only chunk was too small to be a useful retrieval unit.

Decision:

The document title should be treated as document-level metadata rather than a separate retrieval chunk.

---

## Fixed-Size Chunking Experiment

A second experiment used:

- Chunk size: 500 characters
- Overlap: 50 characters

This method produced predictable chunk sizes but several awkward boundaries.

Some chunks:

- Started in the middle of sentences
- Ended in the middle of concepts
- Mixed two different sections
- Split tables or related content across chunks

This showed that fixed-size chunking is useful as a comparison baseline but is not the preferred initial strategy for our current Markdown documents.

---

## Chunking Comparison

| Strategy | Observation |
|---|---|
| Section-based | Cleaner semantic boundaries |
| Fixed-size | Predictable but sometimes cuts concepts |
| Section-based | Better fit for our Markdown structure |
| Fixed-size | Useful as a comparison baseline |

---

## Manual Chunk Inspection

Eight chunks were manually inspected.

Four section-based chunks were reviewed and generally preserved complete concepts.

Four fixed-size chunks were reviewed and several showed awkward boundaries.

Important observations included:

- Some fixed-size chunks started with sentence fragments.
- Some fixed-size chunks mixed the end of one section with the beginning of another.
- Section-based chunks were easier to interpret as retrieval units.
- The section-based approach better preserved meaningful concepts in the current Markdown documents.

---

## Metadata

Metadata provides information about a chunk.

The planned metadata fields are:

- filename
- topic
- section
- chunk_id

Example:

filename = rag-fundamentals.md
topic = RAG
section = What is RAG?
chunk_id = rag-001

Metadata can later help identify the source of retrieved information and support source display or filtering.

---

## Chunking Decision

For the current Markdown knowledge base, the initial preferred method is:

**Section-based chunking using Markdown heading boundaries.**

The document title will be treated as metadata rather than a standalone chunk.

This decision is based on the observed structure and actual chunking experiment results from the project documents.

The final configuration will still be validated during actual RAG retrieval testing.

---

## Day 5 Engineering Lesson

Today I learned that data preparation is an important part of AI engineering.

The final answer quality of a RAG system does not depend only on the LLM.

The overall pipeline is:

Documents
↓
Cleaning
↓
Chunking
↓
Embeddings
↓
Retrieval
↓
Context
↓
LLM
↓
Grounded Answer

Poor documents or poor chunking can lead to poor retrieval and therefore poor answers.

---

## Day 5 Work Completed

- Collected three source documents.
- Checked the source documents for obvious duplicate or irrelevant content.
- Learned chunking concepts.
- Tested section-based chunking.
- Tested fixed-size chunking.
- Tested 500-character chunks with 50-character overlap.
- Compared the two approaches.
- Inspected eight chunks manually.
- Designed chunk metadata.
- Selected section-based chunking as the initial method.
- Documented the experiment and decision.

---

## Next

**Day 6 — Build the First RAG Version**

The next stage is to move from document preparation into the actual RAG pipeline:

Document
↓
Loading
↓
Embedding
↓
Vector Store
↓
Retrieval
↓
Prompt
↓
Response
