
import sys
from pathlib import Path

RETRIEVAL_DIR = Path(__file__).resolve().parent
PDF_PROCESSING_DIR = RETRIEVAL_DIR.parent
PIPELINE_DIR = PDF_PROCESSING_DIR / "pipeline"

for _p in (PDF_PROCESSING_DIR, PIPELINE_DIR, RETRIEVAL_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from qa import answer_question
from summarizer import summarize_paper
from comparision import compare_papers
from paper_extractor import extract_papers

from pipeline.ingest import ingest_pdf, list_papers


app = FastAPI(
    title="ResearchGPT API",
    version="2.0.0",
    description="RAG pipeline for research papers — upload, ask, summarize, compare.",
)


class QuestionRequest(BaseModel):
    question: str
    paper_name: str

class SummaryRequest(BaseModel):
    paper_name: str

class ComparisonRequest(BaseModel):
    question: str
    paper_a: str
    paper_b: str


@app.get("/")
def home():
    return {"message": "ResearchGPT API Running", "version": "2.0.0"}


@app.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    pdf_bytes = await file.read()

    if len(pdf_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    result = ingest_pdf(pdf_bytes, file.filename)

    if result["error"]:
        raise HTTPException(status_code=422, detail=result["error"])

    return JSONResponse(content=result)


@app.get("/papers")
def get_papers():
    papers = list_papers()
    return {"papers": papers}


@app.post("/ask")
def ask(request: QuestionRequest):
    result = answer_question(
        request.question,
        request.paper_name
    )
    return result


@app.post("/summary")
def summary(request: SummaryRequest):
    result = summarize_paper(
        request.paper_name
    )
    return result


@app.post("/compare")
def compare(request: ComparisonRequest):
    answer = compare_papers(
        request.question,
        request.paper_a,
        request.paper_b,
    )
    return {"comparision": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)