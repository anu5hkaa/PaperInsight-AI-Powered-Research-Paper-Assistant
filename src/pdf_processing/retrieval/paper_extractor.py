import sys
import re
from pathlib import Path

_PDF_PROCESSING_DIR = Path(__file__).resolve().parents[1]

if str(_PDF_PROCESSING_DIR) not in sys.path:
    sys.path.insert(0, str(_PDF_PROCESSING_DIR))

from vectordb.chroma_setup import collection


def clean(text):

    text = text.lower()

    text = text.replace(".pdf", "")

    text = re.sub(r"[^a-z0-9 ]", " ", text)

    return " ".join(text.split())


def extract_papers(question):

    question = clean(question)

    results = collection.get(
        include=["metadatas"]
    )

    papers = []

    for meta in results["metadatas"]:

        original_name = meta["paper_name"]

        clean_name = clean(original_name)

        papers.append(
            (clean_name, original_name)
        )

    detected = []

    for clean_name, original_name in papers:

        if clean_name in question:

            detected.append(original_name)

    detected = list(set(detected))

    if len(detected) != 2:

        print("\nDetected Papers:", detected)

        raise ValueError(
            "Unable to detect exactly two papers."
        )

    return detected[0], detected[1]