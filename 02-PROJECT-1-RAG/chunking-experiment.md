# Chunking Experiment

## Objective

Understand how different chunking strategies affect the quality and usefulness of retrieved information in our RAG system.

## Source Document

The experiment was performed on:

- ai-fundamentals.md
- llm-generative-ai.md
- rag-fundamentals.md

## Strategy 1: Section-Based Chunking

Section-based chunking splits Markdown documents using meaningful `##` headings.

### Observation

The section-based approach produced cleaner chunks for our Markdown documents because the existing headings already represent meaningful topic boundaries.

The resulting chunks generally preserved complete concepts and were easier to interpret as retrieval units.

One issue was identified: the top-level document title (`# ...`) should not be treated as a standalone retrieval chunk. It is more useful as document-level metadata.

## Strategy 2: Fixed-Size Chunking

The fixed-size experiment used:

- Chunk size: 500 characters
- Overlap: 50 characters

### Observation

The fixed-size experiment produced several awkward boundaries.

Some chunks ended in the middle of sentences or concepts, which split related information across multiple chunks.

### Example

A fixed-size chunk ended in the middle of a sentence, with the remaining part appearing in the next chunk.

This can make the individual chunks less useful as retrieval context.

## Comparison

| Strategy | Observation |
|---|---|
| Section-based | Cleaner semantic boundaries |
| Fixed-size | Predictable but sometimes cuts concepts |
| Section-based | Better fit for our Markdown structure |
| Fixed-size | Useful as a comparison baseline |

## Decision After Experiment

For the current Markdown knowledge base, section-based chunking is the preferred starting strategy.

The document title should be stored as metadata rather than a separate chunk.

The final configuration will still be validated during the actual RAG retrieval stage.

## Eight-Chunk Inspection

Eight chunks will be manually inspected for:

- Complete meaning
- Sentence boundary quality
- Amount of irrelevant information
- Retrieval usefulness
- Metadata quality
### Manual Inspection Results

Eight chunks were manually inspected: four section-based chunks and four fixed-size chunks.

#### Section-Based Chunks

The inspected section-based chunks generally preserved complete concepts and had clean boundaries.

- `rag-fundamentals.md` — Chunk 1: complete RAG definition and flow.
- `rag-fundamentals.md` — Chunk 6: complete chunking explanation.
- `rag-fundamentals.md` — Chunk 14: complete grounding rule.
- `rag-fundamentals.md` — Chunk 15: complete hallucination explanation.

#### Fixed-Size Chunks

The inspected fixed-size chunks showed several boundary problems.

- Chunk 2 started in the middle of a sentence.
- Chunk 5 started with a sentence fragment.
- Chunk 11 mixed the end of one topic with the beginning of another.
- Chunk 17 split a section/table across chunk boundaries.

#### Inspection Conclusion

Section-based chunking produced cleaner and more self-contained retrieval units for the current Markdown documents.

Fixed-size chunking was useful as a comparison baseline, but the 500-character configuration created several awkward boundaries.

The current implementation will therefore use section-based Markdown headings as the initial chunk boundaries.


## Final Chunking Method

Section-based chunking using Markdown heading boundaries will be used as the initial method for the current document set.

This decision is based on the observed structure of the actual documents rather than an assumed universal best practice.