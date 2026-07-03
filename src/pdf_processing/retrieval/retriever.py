import sys
from pathlib import Path

_PDF_PROCESSING_DIR = Path(__file__).resolve().parents[1]

if str(_PDF_PROCESSING_DIR) not in sys.path:
    sys.path.insert(0, str(_PDF_PROCESSING_DIR))

from sentence_transformers import CrossEncoder
from vectordb.chroma_setup import collection

from embeddings.embedding import get_model as get_embedding_model

_reranker = None


def get_reranker():
    global _reranker

    if _reranker is None:
        _reranker = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    return _reranker


def retrieve_chunks(question, paper_name, n_results=30):

    model = get_embedding_model()

    question_embedding = model.encode(
        "Represent this sentence for searching relevant passage: "
        + question
    )

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=n_results,
        where={
            "paper_name": paper_name
        },
        include=[
            "documents",
            "metadatas"
        ]
    )

    return results


def retrieve_complete_paper(paper_name):

    results = collection.get(
        where={
            "paper_name": paper_name
        },
        include=[
            "documents",
            "metadatas"
        ]
    )

    return results


def retrieve_multiple_papers(question, paper_names):

    all_documents = []
    all_metadata = []

    for paper in paper_names:

        results = retrieve_chunks(
            question,
            paper
        )

        all_documents.extend(
            results["documents"][0]
        )

        all_metadata.extend(
            results["metadatas"][0]
        )

    return {
        "documents": all_documents,
        "metadatas": all_metadata
    }


def rerank_chunks(question, documents):

    pairs = [
        (question, doc)
        for doc in documents
    ]

    reranker = get_reranker()

    scores = reranker.predict(pairs)

    reranked = sorted(
        zip(scores, documents),
        key=lambda x: x[0],
        reverse=True
    )

    return reranked