
from retriever import retrieve_complete_paper
from generator import generate_answer
import time

BATCH_SIZE = 40
MERGE_SIZE = 3


def summarize_batch(context):

    prompt = f"""
You are an expert research assistant.

Summarize the following section of a research paper.

Focus on:

1. Main ideas
2. Methodology
3. Technical concepts
4. Findings
5. Contributions

Context:

{context}
"""

    return generate_answer(prompt)


def merge_summaries(summaries):

    combined = "\n\n".join(summaries)

    prompt = f"""
You are an expert research assistant.

The following are summaries of
different sections of a research paper.

Merge them into a single coherent summary.

Summaries:

{combined}
"""

    return generate_answer(prompt)



def generate_final_summary(
    paper_name,
    merged_summary
):

    prompt = f"""
You are an expert AI research assistant.

Generate a comprehensive summary of the paper.

Paper Name:
{paper_name}

Include:

1. Objective

2. Problem Statement

3. Methodology

4. Architecture

5. Training Procedure

6. Experiments

7. Results

8. Advantages

9. Limitations

10. Applications

11. Final Conclusion

Use ONLY the provided information.

Context:

{merged_summary}
"""

    return generate_answer(prompt)



def summarize_paper(paper_name):

    
    print(
    f"\nSelected Paper: {paper_name}"
)

    
    results = retrieve_complete_paper(
        paper_name
    )

    documents = results["documents"]
    metadatas = results["metadatas"]

    print(
        f"Loaded {len(documents)} chunks."
    )

    batch_summaries = []

    total_batches = (
        len(documents)
        + BATCH_SIZE
        - 1
    ) // BATCH_SIZE

    for i in range(
        0,
        len(documents),
        BATCH_SIZE
    ):

        batch_number = (
            i // BATCH_SIZE
        ) + 1

        print(
            f"\nSummarizing Batch "
            f"{batch_number}/{total_batches}"
        )

        batch_docs = documents[
            i:i + BATCH_SIZE
        ]

        batch_metadata = metadatas[
            i:i + BATCH_SIZE
        ]

        context = "\n\n".join(
            batch_docs
        )

        summary = summarize_batch(
            context
        )
        if summary is None:

            print(
        f"Skipping Batch {batch_number}"
    )

            continue
        batch_summaries.append(
            {
                "summary": summary,
                "metadata": batch_metadata,
                "paper_name": paper_name
            }
        )

        time.sleep(3)

    merged_summaries = []

    for i in range(
        0,
        len(batch_summaries),
        MERGE_SIZE
    ):

        group = batch_summaries[
            i:i + MERGE_SIZE
        ]

        summaries = [
            item["summary"]
            for item in group
        ]

        merged_summary = merge_summaries(
            summaries
        )
        if merged_summary is None:

            continue
        merged_summaries.append(
            merged_summary
        )

        time.sleep(3)



    final_context = "\n\n".join(
        merged_summaries
    )

    print(
        "\nGenerating Final Summary..."
    )
    if len(merged_summaries) == 0:

        return {
        "paper_name": paper_name,
        "summary": "Unable to generate summary because all Gemini requests failed.",
        "chunks_used": len(documents),
        "batch_summaries": batch_summaries
    }

    final_summary = generate_final_summary(
        paper_name,
        final_context
    )
    if final_summary is None:

        final_summary = (
        "Final summary generation failed."
    )

    
    return {
        "paper_name": paper_name,
        "summary": final_summary,
        "chunks_used": len(documents),
        "batch_summaries": batch_summaries
    }