import json
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def create_chunks(
    text_file: str | Path,
    output_dir: str | Path = PROJECT_ROOT / "data" / "chunks"
):
    """
    Reads extracted text and creates overlapping chunks.

    Returns:
        output_path
        chunks
    """

    text_file = Path(text_file)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paper_name = text_file.stem

    with open(
        text_file,
        "r",
        encoding="utf-8"
    ) as f:
        text = f.read()

    text = " ".join(text.split())

    chunks = []

    start = 0
    chunk_id = 0

    while start < len(text):

        end = start + CHUNK_SIZE

        chunk = text[start:end]

        chunks.append(
            {
                "chunk_id": chunk_id,
                "paper_name": paper_name,
                "text": chunk
            }
        )

        chunk_id += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP

    output_path = output_dir / f"{paper_name}_chunks.json"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

    return output_path, chunks


if __name__ == "__main__":

    file = input("Enter extracted text path: ")

    output_path, chunks = create_chunks(file)

    print(f"\nCreated {len(chunks)} chunks.")
    print(f"Saved to: {output_path}")