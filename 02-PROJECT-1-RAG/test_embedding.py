from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

text = "What is Retrieval-Augmented Generation?"

embedding = model.encode(text)

print("Text:")
print(text)

print("\nEmbedding type:")
print(type(embedding))

print("\nEmbedding dimensions:")
print(len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])