"""
ingest.py
---------
ResearchGPT Ingestion Pipeline

Upload PDF
    ↓
Extract Text
    ↓
Chunk Text
    ↓
Generate Embeddings
    ↓
Store in ChromaDB
"""

from pathlib import Path

# ==========================================================
# Import reusable modules
# ==========================================================

from extractor import extract_text
from chunking.chunking import create_chunks
from embeddings.embedding import generate_embeddings
from vectordb.chroma_setup import (
    insert_embeddings,
    list_papers,
    paper_exists,
)

# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==========================================================
# Save Uploaded PDF
# ==========================================================

def save_uploaded_pdf(
    pdf_bytes: bytes,
    filename: str,
):
    pdf_path = UPLOAD_DIR / filename

    pdf_path.write_bytes(pdf_bytes)

    return pdf_path


# ==========================================================
# Main Pipeline
# ==========================================================

def ingest_pdf(
    pdf_bytes: bytes,
    filename: str,
):

    paper_name = (
        Path(filename)
        .stem
        .lower()
        .strip()
    )

    print("=" * 60)
    print("INGESTING:", paper_name)
    print("=" * 60)

    if paper_exists(paper_name):
        return {
            "paper_name": paper_name,
            "chunks": 0,
            "inserted": 0,
            "already_existed": True,
            "error": None,
        }

    try:

        # ----------------------------------------------------
        # Save uploaded PDF
        # ----------------------------------------------------

        pdf_path = save_uploaded_pdf(
            pdf_bytes,
            filename,
        )

        # ----------------------------------------------------
        # Step 1 : Extract Text
        # ----------------------------------------------------

        text_file, text = extract_text(str(
            pdf_path
        ))

        if not text.strip():
            return {
                "paper_name": paper_name,
                "chunks": 0,
                "inserted": 0,
                "already_existed": False,
                "error": "Could not extract text from PDF.",
            }

        print(
            f"Characters extracted: {len(text)}"
        )

        # ----------------------------------------------------
        # Step 2 : Chunking
        # ----------------------------------------------------

        chunk_file, chunks = create_chunks(
            text_file
        )

        print(
            f"Chunks created: {len(chunks)}"
        )

        # ----------------------------------------------------
        # Step 3 : Embeddings
        # ----------------------------------------------------

        embedding_file, embeddings = generate_embeddings(
            chunk_file
        )

        print(
            f"Embeddings created: {len(embeddings)}"
        )

        # ----------------------------------------------------
        # Step 4 : ChromaDB
        # ----------------------------------------------------

        inserted, total_chunks = insert_embeddings(
            embedding_file
        )

        print(
            f"Inserted: {inserted}"
        )

        print(
            f"Total Chunks in DB: {total_chunks}"
        )

        return {
            "paper_name": paper_name,
            "chunks": len(chunks),
            "inserted": inserted,
            "already_existed": False,
            "error": None,
        }

    except Exception as e:
        return {
            "paper_name": paper_name,
            "chunks": 0,
            "inserted": 0,
            "already_existed": False,
            "error": str(e),
        }