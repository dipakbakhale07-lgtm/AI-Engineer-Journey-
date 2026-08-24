from pathlib import Path

DOCUMENTS_DIR = Path("documents")

CHUNK_SIZE = 500
OVERLAP = 50


def section_based_chunks(text):
    """
    Split Markdown into sections using level-2 headings.
    The document title (# ...) is treated as metadata,
    not as a chunk.
    """
    lines = text.strip().splitlines()

    chunks = []
    current = []

    for line in lines:
        if line.startswith("## "):
            if current:
                chunks.append("\n".join(current).strip())
            current = [line]
        elif not current:
            # Skip the top-level document title from chunk content.
            continue
        else:
            current.append(line)

    if current:
        chunks.append("\n".join(current).strip())

    return [chunk for chunk in chunks if chunk]


def fixed_size_chunks(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Split text into fixed-size character chunks with overlap.
    """
    text = text.strip()
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


for file_path in DOCUMENTS_DIR.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")

    section_chunks = section_based_chunks(text)
    fixed_chunks = fixed_size_chunks(text)

    print("\n" + "=" * 70)
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    print("\nSECTION-BASED CHUNKING")
    print("-" * 70)

    for index, chunk in enumerate(section_chunks, start=1):
        print(f"\nChunk {index} | Characters: {len(chunk)}")
        print(chunk)

    print("\nFIXED-SIZE CHUNKING")
    print("-" * 70)

    for index, chunk in enumerate(fixed_chunks, start=1):
        print(f"\nChunk {index} | Characters: {len(chunk)}")
        print(chunk)