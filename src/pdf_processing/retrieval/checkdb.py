import sys
from pathlib import Path

_PDF_PROCESSING_DIR = Path(__file__).resolve().parents[1]

if str(_PDF_PROCESSING_DIR) not in sys.path:
    sys.path.insert(0, str(_PDF_PROCESSING_DIR))

from vectordb.chroma_setup import client, collection

print("Collections:", client.list_collections())
print("Total Chunks:", collection.count())

data = collection.get(include=["metadatas"])

papers = sorted(
    set(meta["paper_name"] for meta in data["metadatas"])
)

print("\nStored Papers:")
print(papers)

bert = collection.get(
    where={"paper_name": "bert"},
    include=["documents"]
)

print("\nBERT Chunks:", len(bert["documents"]))