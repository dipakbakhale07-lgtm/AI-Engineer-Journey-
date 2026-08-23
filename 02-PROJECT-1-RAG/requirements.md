### Document Loader

### Chunking Component

### Embedding Model

### Vector Store

### Retriever

### LLM

### Source Information

# Project 1 — RAG Knowledge Assistant

## 1. Problem Statement

People often need to find specific information from a collection of documents, but manually searching through multiple files can be slow and inconvenient.

The goal of this project is to build a document-based RAG Knowledge Assistant that allows a user to ask questions in natural language and receive answers based on information retrieved from the approved documents.

The assistant should focus on retrieving relevant information before generating the final answer, rather than relying only on the language model's general knowledge.

## 2. Target User

The primary user is a learner or student who wants to quickly find reliable information from a defined collection of AI and AI-engineering learning documents.

The assistant should reduce the time required to manually search through multiple documents and make relevant information easier to access.

---

## 3. Project Scope

### The assistant should:

- Accept questions in natural language.
- Search the approved document collection.
- Retrieve relevant document chunks.
- Use the retrieved context to generate an answer.
- Provide source information for the answer.
- Accept questions outside the predefined evaluation questions.
- Clearly indicate when the required information cannot be found in the provided documents.

### The assistant should not:

- Invent information that is not supported by the provided documents.
- Treat the predefined test questions as the only questions users can ask.
- Use unapproved documents as a knowledge source.
- Claim that an answer is supported when the required evidence cannot be retrieved.

---

## 4. Core Project Rule

The assistant should answer using information supported by the provided documents.

When sufficient supporting information cannot be found, the assistant should respond:

> "I could not find this information in the provided documents."

## 5. Knowledge Source

The RAG Knowledge Assistant will use a controlled collection of approved documents as its knowledge source.

The initial knowledge domain will focus on AI and AI-engineering learning material.

The document collection may include:

- AI concepts and explanations
- RAG concepts and explanations
- AI agent concepts and explanations
- Sample AI course FAQ material

The assistant should use only the documents that are intentionally added to the project knowledge base.

---

## 6. Document Strategy

The first version will use a small, controlled document collection so that the retrieval and grounding behavior can be properly tested.

The document collection will be prepared during the document-preparation stage of the project.

The documents will later be:

1. Loaded into the RAG pipeline.
2. Cleaned where necessary.
3. Divided into smaller chunks.
4. Converted into embeddings.
5. Stored in the selected vector store.
6. Retrieved when a user asks a question.

The document set will also include a second, messier batch for stress testing during the document-preparation stage.

## 7. RAG Architecture

The RAG Knowledge Assistant will use a retrieval-augmented generation architecture.

### Document Ingestion Flow

```text
Approved Documents
        ↓
Document Loading
        ↓
Text Cleaning
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Store
        
## Question Answering Flow
User Question
        ↓
Question Processing
        ↓
Retrieval
        ↓
Relevant Document Chunks
        ↓
Context + User Question
        ↓
LLM
        ↓
Grounded Answer
        ↓
Source Information

Complete System Flow
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │     RAG App      │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │  User Question   │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │    Retriever     │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │   Vector Store   │
                         └────────┬─────────┘
                                  ↓
                           Relevant Chunks
                                  ↓
                         ┌──────────────────┐
                         │       LLM        │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ Grounded Answer  │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ Source Information│
                         └──────────────────┘
Main System Flow
Documents
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector Store
   ↓
User Question
   ↓
Retrieval
   ↓
Relevant Context
   ↓
LLM
   ↓
Grounded Answer
   ↓
Source Information 

## 8. Main System Components
### Document Loader

Loads the approved documents into the RAG pipeline.

### Chunking Component

Splits documents into smaller pieces so that relevant information can be retrieved efficiently.

### Embedding Model

Converts document chunks and user questions into vector representations.

### Vector Store

Stores the document embeddings and supports similarity-based retrieval.

### Retriever

Searches the vector store and returns relevant document chunks for the user's question.

### LLM

Uses the user's question together with the retrieved context to generate the final response.

### Source Information

The application should provide information about the source used for the answer whenever practical.