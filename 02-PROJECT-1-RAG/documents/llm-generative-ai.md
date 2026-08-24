# LLM and Generative AI

## What is Generative AI?

Generative AI refers to artificial intelligence systems capable of creating new content based on a given input or prompt.
This type of AI can produce various forms of output, including:

- Written text
- Visual images
- Audio clips
- Video sequences
- Computer code

It’s important to note that generative AI does not automatically update or retrain itself as a result of user interactions. Each input is processed independently, without persistent learning from individual exchanges.

## What is an LLM?

LLM stands for Large Language Model.

An LLM is a machine learning model trained on vast quantities of textual data, enabling it to understand and generate human-like language.
Common uses of LLMs include:

- Answering questions
- Summarizing long texts
- Translating between languages
- Generating written content
- Writing or completing code
These models excel at processing language patterns but do not inherently "know" facts—they predict likely word sequences based on training data.

## LLM vs AI Application

An LLM is fundamentally a standalone model.

In contrast, an AI application typically integrates an LLM with additional components to enhance functionality. These may include:
- Stored documents
- Retrieval systems
- External tools
- APIs
- Custom logic
- User interfaces

For instance:

LLM
↓
Basic language model

RAG Application
↓
Documents + Retrieval System + LLM + Application Logic
This combination allows for more accurate, context-aware responses by grounding the model in external information.

## What is an Embedding?

An embedding is a technique that transforms data—such as words or sentences—into numerical vectors that reflect their semantic meaning.

Example:

"How does RAG work?"
↓
Embedding Model
↓
Numerical Vector

While the resulting numbers aren’t meant to be interpreted directly by humans, they allow machines to measure how closely related different pieces of content are in meaning.

## Why Are Embeddings Useful in RAG?

In RAG systems, embeddings enable the identification of information that is conceptually similar to a user’s query, even when exact wording differs.

For example:

Document:
"RAG retrieves relevant information from a knowledge source."

Question:
"How does a RAG system find information?"

Though the phrasing varies, the underlying meaning is aligned.
By converting both the document and the question into vector form, the system can detect this semantic similarity and retrieve the most relevant content accordingly.

## RAG

RAG stands for Retrieval-Augmented Generation.

A simplified RAG process looks like this:

Documents
↓
Split into Chunks
↓
Converted into Embeddings
↓
Stored in a Vector Database
↓
Searched for Similarity to Query
↓
Relevant Text Chunks Retrieved
↓
Passed to LLM
↓
Generates a Contextually Grounded Response