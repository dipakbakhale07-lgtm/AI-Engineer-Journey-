from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


DOCUMENTS_PATH = Path("documents")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5


def section_based_chunks(text):
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


def cosine_similarity(query_vector, document_vectors):
    query_norm = np.linalg.norm(query_vector)

    document_norms = np.linalg.norm(
        document_vectors,
        axis=1
    )

    return np.dot(
        document_vectors,
        query_vector
    ) / (
        document_norms * query_norm
    )


documents = []

for file_path in sorted(DOCUMENTS_PATH.glob("*.md")):
    documents.append({
        "filename": file_path.name,
        "text": file_path.read_text(
            encoding="utf-8"
        )
    })


database = []

for document in documents:

    chunks = section_based_chunks(
        document["text"]
    )

    for chunk in chunks:

        database.append({
            "filename": document["filename"],
            "text": chunk
        })


print("=" * 70)
print("Q21 RETRIEVAL DIAGNOSTIC")
print("=" * 70)

question = "Does using RAG guarantee that an LLM will never hallucinate?"

print("\nQUESTION:")
print(question)

print("\nLoading local embedding model...")

model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

texts = [
    item["text"]
    for item in database
]

embeddings = model.encode(texts)

query_embedding = model.encode(
    question
)

scores = cosine_similarity(
    query_embedding,
    embeddings
)

ranked_indices = np.argsort(
    scores
)[::-1]

print("\nTOP 5 RETRIEVED CHUNKS")
print("=" * 70)

for rank, index in enumerate(
    ranked_indices[:TOP_K],
    start=1
):

    item = database[index]

    print(
        f"\nRank {rank}"
    )

    print(
        f"Similarity: "
        f"{scores[index]:.4f}"
    )

    print(
        f"Source: "
        f"{item['filename']}"
    )

    print("-" * 70)

    print(
        item["text"]
    )

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)