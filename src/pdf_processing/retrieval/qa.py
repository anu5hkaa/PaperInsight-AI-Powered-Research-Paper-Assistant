
from retriever import retrieve_chunks
from retriever import rerank_chunks
from promt_builder import build_qa_prompt
from generator import generate_answer


TOP_K = 5


def answer_question(question,paper_name):

    print(
    f"\nSelected Paper: {paper_name}"
)

  
    results = retrieve_chunks(
        question,
        paper_name
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    print(
        f"Retrieved {len(documents)} chunks."
    )

    reranked = rerank_chunks(
        question,
        documents
    )

   
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

    prompt = build_qa_prompt(
        question,
        context
    )

    
    answer = generate_answer(
        prompt
    )

    
    return {
        "paper_name": paper_name,
        "answer": answer,
        "sources": top_docs,
        "metadata": metadatas
    }