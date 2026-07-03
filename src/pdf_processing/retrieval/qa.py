
from retriever import retrieve_chunks
from retriever import rerank_chunks
from promt_builder import build_qa_prompt
from generator import generate_answer


TOP_K = 5


def answer_question(question,paper_name):

    # =====================================
    # STEP 1 : Detect Paper
    # =====================================

    print(
    f"\nSelected Paper: {paper_name}"
)

    # =====================================
    # STEP 2 : Retrieve Chunks
    # =====================================

    results = retrieve_chunks(
        question,
        paper_name
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    print(
        f"Retrieved {len(documents)} chunks."
    )

    # =====================================
    # STEP 3 : Rerank
    # =====================================

    reranked = rerank_chunks(
        question,
        documents
    )

    # =====================================
    # STEP 4 : Top Documents
    # =====================================

    top_docs = []

    
    for score, doc in reranked[:TOP_K]:

        doc_index = documents.index(doc)

        top_docs.append(
            {
                "document": doc,
                "metadata": metadatas[doc_index],
                "score": float(score)
            }
        )

    context = "\n\n".join(
    item["document"]
    for item in top_docs
)

    # =====================================
    # STEP 5 : Prompt
    # =====================================

    prompt = build_qa_prompt(
        question,
        context
    )

    # =====================================
    # STEP 6 : Gemini
    # =====================================

    answer = generate_answer(
        prompt
    )

    # =====================================
    # STEP 7 : Return
    # =====================================

    return {
        "paper_name": paper_name,
        "answer": answer,
        "sources": top_docs,
        "metadata": metadatas
    }