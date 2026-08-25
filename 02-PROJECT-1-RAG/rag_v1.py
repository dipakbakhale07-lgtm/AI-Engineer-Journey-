from pathlib import Path

import numpy as np
import requests
from sentence_transformers import SentenceTransformer


DOCUMENT_PATH = Path("documents/rag-fundamentals.md")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3:latest"

TOP_K = 3


def load_document(file_path: Path) -> str:
    """Read a UTF-8 Markdown file and return its contents."""
    if not file_path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    return file_path.read_text(encoding="utf-8")


def section_based_chunks(text: str) -> list[str]:
    """Split Markdown content using level-2 headings."""

    lines = text.strip().splitlines()

    chunks = []
    current = []

    for line in lines:
        if line.startswith("## "):

            if current:
                chunks.append("\n".join(current).strip())

            current = [line]

        elif not current:
            continue

        else:
            current.append(line)

    if current:
        chunks.append("\n".join(current).strip())

    return [chunk for chunk in chunks if chunk]


def cosine_similarity(
    query_vector: np.ndarray,
    document_vectors: np.ndarray
) -> np.ndarray:
    """Calculate cosine similarity between query and document vectors."""

    query_norm = np.linalg.norm(query_vector)
    document_norms = np.linalg.norm(document_vectors, axis=1)

    return np.dot(document_vectors, query_vector) / (
        document_norms * query_norm
    )


def build_context(
    chunks: list[str],
    indices: np.ndarray
) -> str:
    """Combine retrieved chunks into one context string."""

    retrieved_chunks = []

    for index in indices:
        retrieved_chunks.append(chunks[index])

    return "\n\n---\n\n".join(retrieved_chunks)


def generate_answer(question: str, context: str) -> str:
    """Send the grounded prompt to the local Ollama model."""

    prompt = f"""
You are a RAG question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the provided context,
say:

"I could not find this information in the provided documents."

Do not use outside knowledge.
Do not guess.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()


def main() -> None:

    # 1. Load document
    text = load_document(DOCUMENT_PATH)

    # 2. Create chunks
    chunks = section_based_chunks(text)

    print("=" * 60)
    print("DOCUMENT")
    print("=" * 60)

    print(f"File: {DOCUMENT_PATH.name}")
    print(f"Characters: {len(text)}")
    print(f"Chunks: {len(chunks)}")

    # 3. Load embedding model
    print("\nLoading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # 4. Embed document chunks
    embeddings = model.encode(chunks)

    print(f"Embedding shape: {embeddings.shape}")

    # 5. User question
    question = "What is RAG?"

    print("\n" + "=" * 60)
    print("QUESTION")
    print("=" * 60)

    print(question)

    # 6. Embed question
    query_embedding = model.encode(question)

    # 7. Similarity search
    scores = cosine_similarity(
        query_embedding,
        embeddings
    )

    # 8. Rank chunks
    ranked_indices = np.argsort(scores)[::-1]

    top_indices = ranked_indices[:TOP_K]

    # 9. Inspect retrieval
    print("\n" + "=" * 60)
    print("RETRIEVED CHUNKS")
    print("=" * 60)

    for rank, index in enumerate(top_indices, start=1):

        print(f"\nRank {rank}")
        print(f"Similarity: {scores[index]:.4f}")
        print(f"Chunk ID: rag-{index + 1:03d}")
        print("-" * 60)
        print(chunks[index])

    # 10. Build context
    context = build_context(
        chunks,
        top_indices
    )

    print("\n" + "=" * 60)
    print("CONTEXT SENT TO LLM")
    print("=" * 60)

    print(context)

    # 11. Generate grounded answer
    print("\n" + "=" * 60)
    print("LLM ANSWER")
    print("=" * 60)

    answer = generate_answer(
        question,
        context
    )

    print(answer)


if __name__ == "__main__":
    main()