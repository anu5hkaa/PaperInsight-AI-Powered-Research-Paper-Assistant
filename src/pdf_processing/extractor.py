"""
extractor.py
------------
Extracts raw text from an uploaded PDF and saves it to data/extracted/<paper_name>.txt

Upload PDF -> Extract Text -> Save TXT (this module)
"""

from pathlib import Path
from pypdf import PdfReader

# ==========================================================
# Paths
# ==========================================================
# extractor.py lives directly in src/pdf_processing/, so:
# parents[0] = pdf_processing, parents[1] = src, parents[2] = PROJECT_ROOT
PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXTRACTED_DIR = PROJECT_ROOT / "data" / "extracted"
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)


def extract_text(pdf_path: str | Path, output_dir: str | Path = EXTRACTED_DIR):
    """
    Reads a PDF file and extracts its full text content.

    Saves the extracted text to data/extracted/<paper_name>.txt
    using a normalized (lowercase, stripped) paper name so that it
    stays consistent with chunking / embeddings / ChromaDB metadata.

    Returns:
        output_path (Path)
        text (str)
    """

    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paper_name = pdf_path.stem.lower().strip()

    reader = PdfReader(str(pdf_path))

    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages_text.append(page_text)

    text = "\n".join(pages_text)

    output_path = output_dir / f"{paper_name}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return output_path, text


if __name__ == "__main__":

    pdf_file = input("Enter PDF path: ")

    output_path, text = extract_text(pdf_file)

    print(f"\nExtracted {len(text)} characters.")
    print(f"Saved to: {output_path}")
