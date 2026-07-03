import sys
from pathlib import Path

_PDF_PROCESSING_DIR = Path(__file__).resolve().parents[1]

if str(_PDF_PROCESSING_DIR) not in sys.path:
    sys.path.insert(0, str(_PDF_PROCESSING_DIR))

from vectordb.chroma_setup import collection

from embeddings.embedding import get_model as get_embedding_model


def classify_paper(question):

    embedding_model = get_embedding_model()

    question_embedding = embedding_model.encode(
        "Represent this sentence for searching relevant passage: "
        + question
    )

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=10,
        include=["metadatas"]
    )

    paper_count = {}

    for meta in results["metadatas"][0]:

        paper = meta["paper_name"]

        paper_count[paper] = (
            paper_count.get(paper, 0) + 1
        )

    predicted_paper = max(
        paper_count,
        key=paper_count.get
    )

    return predicted_paper