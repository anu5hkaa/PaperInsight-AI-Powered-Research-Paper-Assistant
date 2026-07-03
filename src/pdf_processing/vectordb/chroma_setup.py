import chromadb
import json
from pathlib import Path

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client.get_or_create_collection(
    name="research_papers"
)

# ==========================================================
# Insert Embeddings
# ==========================================================

def insert_embeddings(embedding_file):

    embedding_file = Path(embedding_file)

    with open(
        embedding_file,
        "r",
        encoding="utf-8"
    ) as f:
        embeddings_data = json.load(f)

    inserted = 0

    for item in embeddings_data:

        unique_id = (
            f"{item['paper_name']}_{item['chunk_id']}"
        )

        existing = collection.get(
            ids=[unique_id]
        )

        if existing["ids"]:
            continue

        collection.add(
            ids=[unique_id],
            embeddings=[item["embedding"]],
            documents=[item["text"]],
            metadatas=[
                {
                    "chunk_id": item["chunk_id"],
                    "paper_name": item["paper_name"]
                }
            ]
        )

        inserted += 1

    return inserted, collection.count()

# ==========================================================
# Check if Paper Exists
# ==========================================================

def paper_exists(paper_name):

    results = collection.get(
        where={
            "paper_name": paper_name
        },
        include=["metadatas"]
    )

    return len(results["ids"]) > 0
# ==========================================================
# List Papers
# ==========================================================

def list_papers():

    results = collection.get(
        include=["metadatas"]
    )

    papers = sorted(
        set(
            m["paper_name"]
            for m in results["metadatas"]
        )
    )

    return papers


# ==========================================================
# Run Directly
# ==========================================================

if __name__ == "__main__":

    embedding_file = input(
        "Enter embedding json path: "
    )

    inserted, total = insert_embeddings(
        embedding_file
    )

    print("\nInserted:", inserted)
    print("Total Chunks:", total)