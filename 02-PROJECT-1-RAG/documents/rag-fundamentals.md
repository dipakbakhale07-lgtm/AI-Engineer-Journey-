# RAG Fundamentals

## What is RAG?

RAG stands for Retrieval-Augmented Generation.

RAG is a system architecture that retrieves relevant information from a knowledge source and provides that information to a Large Language Model (LLM) before generating an answer.

A simplified RAG flow is:

User Question
↓
Retrieve Relevant Information
↓
Relevant Context
↓
LLM
↓
Generated Answer

## Why is RAG Needed?

An LLM has knowledge learned during its training, but an application may need to answer questions using specific documents or a private knowledge base.

RAG allows the application to retrieve relevant information from those documents and provide it to the LLM as context.

For example:

User:
"What are the prerequisites mentioned in our course FAQ?"

Instead of relying only on the LLM's general knowledge, the RAG system retrieves the relevant section from the course FAQ and gives it to the LLM.

## RAG is an Architecture

RAG is not simply another LLM model.

A RAG application combines multiple components:

- Documents
- Document processing
- Chunking
- Embedding model
- Vector store
- Retrieval
- Context construction
- LLM
- Application logic

Therefore:

LLM
↓
Model

RAG Application
↓
Documents + Retrieval + LLM + Application Logic

## What is a Document?

A document is a source of knowledge that the RAG system can use.

Examples in this project include:

- AI fundamentals
- LLM and Generative AI
- RAG fundamentals
- AI agents
- AI course FAQ

Documents are the original knowledge sources before they are processed for retrieval.

## What is a Chunk?

A chunk is a smaller piece of a document.

Instead of treating a large document as one unit, it can be divided into smaller meaningful pieces.

Example:

Document
├── Chunk 1
├── Chunk 2
├── Chunk 3
├── Chunk 4
└── ...

Chunks allow the retrieval system to find specific relevant sections instead of treating the entire document as one piece.

## What is Chunking?

Chunking is the process of dividing documents into smaller pieces for processing and retrieval.

The chunk size matters.

If chunks are too small:
- Important context can be separated.
- Meaning can become fragmented.
- Retrieved information may be incomplete.

If chunks are too large:
- Retrieved context may contain unnecessary information.
- Relevant information can become mixed with unrelated information.
- Retrieval can become less precise.

Therefore, chunking requires experimentation and inspection rather than blindly choosing one value.

## What is Metadata?

Metadata is information that describes a piece of data.

A chunk can contain metadata such as:

- File name
- Topic
- Section

Example:

Chunk:
"RAG retrieves relevant information..."

Metadata:
filename = rag-fundamentals.md
topic = RAG

Metadata helps identify where retrieved information came from and can also support filtering or source display.

## What is an Embedding?

An embedding is a numerical vector representation of information such as text that captures semantic meaning.

A simplified process is:

Text
↓
Embedding Model
↓
Numerical Vector

The numerical values are not normally interpreted manually.

They are used by AI systems to compare semantic relationships between pieces of information.

## What is a Vector?

A vector is an ordered collection of numerical values.

Example:

[0.12, -0.43, 0.81, 0.27]

An embedding is represented as a vector.

Real embedding models can produce vectors with many dimensions.

## What is a Vector Store?

A vector store is a system used to store and search vector embeddings.

Conceptually:

Chunk 1 → Embedding 1
Chunk 2 → Embedding 2
Chunk 3 → Embedding 3
Chunk 4 → Embedding 4
↓
Vector Store

The vector store allows the system to search for vectors that are semantically similar to a query.

## What is Retrieval?

Retrieval means finding the information that is most relevant to a user's question.

Example:

User:
"What is an embedding?"

↓
Retrieval

↓
Relevant chunk:
"An embedding converts information into a numerical vector representation..."

The retrieved chunk becomes context for the LLM.

## What is Similarity Search?

Similarity search is the process of comparing a query embedding with stored embeddings to find semantically relevant information.

A simplified process is:

User Question
↓
Question Embedding
↓
Compare with Stored Vectors
↓
Find Relevant Vectors
↓
Return Corresponding Chunks

Similarity does not simply mean matching the same words.

It is based on relationships between numerical vector representations.

## What is Context?

Context is the relevant information retrieved from the knowledge base and provided to the LLM.

Example:

Question:
"What is an embedding?"

Retrieved Context:
"An embedding converts information into a numerical vector representation that captures semantic meaning."

Then:

Question + Context
↓
LLM
↓
Answer

## What is Grounding?

Grounding means generating an answer based on the retrieved evidence or context.

For this project, the system should follow a grounding rule:

If the answer exists in the provided documents:
→ Answer using the retrieved evidence.

If the answer cannot be found in the provided documents:
→ Say that the information could not be found in the provided documents.

This prevents the system from freely inventing information when the knowledge source does not contain an answer.

## What is Hallucination?

In an AI system, a hallucination occurs when an LLM generates information that is not supported by the available evidence and presents it as an answer.

Example of an unwanted flow:

Question
↓
No supporting information
↓
LLM guesses
↓
Unsupported Answer

Desired flow:

Question
↓
Retrieve information
↓
Supporting information found
↓
LLM generates grounded answer

If supporting information cannot be found:

Question
↓
No supporting information
↓
Safe fallback response

## Complete RAG Pipeline

### Knowledge Preparation

Documents
↓
Cleaning
↓
Chunking
↓
Embeddings
↓
Vector Store

### Question and Retrieval

User Question
↓
Question Embedding
↓
Vector Store Search
↓
Relevant Chunks
↓
Context

### Generation

Context + User Question
↓
LLM
↓
Grounded Answer
↓
Source / Evidence

## Complete System

Documents
↓
Cleaning
↓
Chunking
↓
Embeddings
↓
Vector Store
↑
│
User Question
↓
Question Embedding
↓
Retrieval
↓
Relevant Chunks
↓
Context
↓
LLM
↓
Grounded Answer
↓
Source / Evidence

## Why Not Send the Entire Document to the LLM?

A RAG system is designed to retrieve relevant information instead of automatically sending the entire knowledge base with every question.

The general idea is:

Question
↓
Find Relevant Information
↓
Send Relevant Context
↓
LLM
↓
Answer

This makes the system focused on the information relevant to the current question.

## Common RAG Failure Points

### 1. Poor Source Documents

Bad or irrelevant source material can lead to poor retrieval.

### 2. Poor Chunking

Chunks that are too small or too large can reduce retrieval quality.

### 3. Poor Retrieval

The system may retrieve irrelevant chunks.

### 4. Unsupported Generation

The LLM may generate an answer that is not supported by the retrieved context.

### 5. Missing Grounding Rule

Without a clear fallback behavior, the system may guess when the documents do not contain the answer.

## Key RAG Components

| Component | Purpose |
|---|---|
| Documents | Provide the knowledge |
| Chunking | Divide documents into smaller pieces |
| Metadata | Describe and identify chunks |
| Embeddings | Represent semantic meaning numerically |
| Vector Store | Store and search embeddings |
| Retrieval | Find relevant chunks |
| Context | Provide retrieved information to the LLM |
| LLM | Generate the final response |
| Grounding | Keep the answer based on available evidence |

## Key Learning

RAG is not simply connecting an LLM to a document.

It is a complete pipeline involving:

Data
→ Processing
→ Chunking
→ Embeddings
→ Retrieval
→ Context
→ LLM
→ Grounded Generation

The quality of the final answer depends not only on the LLM, but also on the quality of the documents, chunks, embeddings, retrieval and grounding process.