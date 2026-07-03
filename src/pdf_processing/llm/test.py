from sentence_transformers import CrossEncoder

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

question = "Who proposed scaled dot-product attention?"

chunks = [
    "Attention is a mechanism used in neural machine translation...",
    "Noam proposed scaled dot-product attention...",
    "Transformer models rely on attention..."
]

pairs = [(question, chunk) for chunk in chunks]

scores = reranker.predict(pairs)

for chunk, score in zip(chunks, scores):
    print("\nScore:", score)
    print(chunk)