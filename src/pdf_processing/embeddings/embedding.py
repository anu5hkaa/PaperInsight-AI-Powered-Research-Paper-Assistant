import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[3]

EMBEDDING_DIR = PROJECT_ROOT / "data" / "embeddings"
EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)

_model = None


def get_model():
    global _model

    if _model is None:
        _model = SentenceTransformer(
            "BAAI/bge-base-en-v1.5"
        )

    return _model


def generate_embeddings(chunk_file):

    chunk_file = Path(chunk_file)

    paper_name = chunk_file.stem.replace(
        "_chunks",
        ""
    )

    with open(
        chunk_file,
        "r",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)

    all_embeddings = []

    model = get_model()

    for chunk in chunks:

        embedding = model.encode(
            chunk["text"]
        )

        all_embeddings.append(
            {
                "chunk_id": chunk["chunk_id"],
                "paper_name": chunk["paper_name"],
                "text": chunk["text"],
                "embedding": embedding.tolist()
            }
        )

    embedding_file = (
        EMBEDDING_DIR /
        f"{paper_name}_embeddings.json"
    )

    with open(
        embedding_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_embeddings,
            f,
            indent=4,
            ensure_ascii=False
        )

    return embedding_file, all_embeddings


if __name__ == "__main__":

    chunk_file = input(
        "Enter chunk file path: "
    )

    embedding_file, embeddings = generate_embeddings(
        chunk_file
    )

    print(
        f"\nGenerated {len(embeddings)} embeddings."
    )

    print(
        f"Saved to: {embedding_file}"
    )