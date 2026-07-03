from retriever import (
    retrieve_complete_paper,
    retrieve_chunks,
    rerank_chunks
)

from generator import generate_answer
from promt_builder import build_comparison_prompt
from comparision_router import detect_comparison_type
from summarizer import summarize_paper
from promt_builder import  build_specific_comparison_prompt
TOP_K = 15


def compare_using_summaries(
    paper_a,
    paper_b
):

    print(
        "\nGenerating summary for Paper A..."
    )

    summary_a = summarize_paper(
        paper_a
    )

    print(
        "\nGenerating summary for Paper B..."
    )

    summary_b = summarize_paper(
        paper_b
    )

    context = f"""



Paper Name:
{paper_a}

Summary:

{summary_a["summary"]}




Paper Name:
{paper_b}

Summary:

{summary_b["summary"]}

"""

    prompt = build_comparison_prompt(
        context
    )

    return generate_answer(
        prompt
    )


def compare_using_retrieval(
    question,
    paper_a,
    paper_b
):

    print(
        "\nUsing Retrieval-Based Comparison..."
    )

    results_a = retrieve_chunks(
        question,
        paper_a
    )

    results_b = retrieve_chunks(
        question,
        paper_b
    )

    docs_a = results_a["documents"][0]
    docs_b = results_b["documents"][0]

    reranked_a = rerank_chunks(
        question,
        docs_a
    )

    reranked_b = rerank_chunks(
        question,
        docs_b
    )

    top_a = "\n\n".join(
        doc
        for score, doc in reranked_a[:TOP_K]
    )

    top_b = "\n\n".join(
        doc
        for score, doc in reranked_b[:TOP_K]
    )

    context = f"""

PAPER A:
{paper_a}

{top_a}


PAPER B:
{paper_b}

{top_b}

"""

    prompt = build_specific_comparison_prompt(
    question,
    context
)

    return generate_answer(
        prompt
    )


def compare_papers(
    question,
    paper_a,
    paper_b
):

    comparison_type = (
        detect_comparison_type(
            question
        )
    )

    print(
        f"\nComparison Type: {comparison_type}"
    )

    if comparison_type == "specific":

        return compare_using_retrieval(
            question,
            paper_a,
            paper_b
        )

    return compare_using_summaries(
        paper_a,
        paper_b
    )