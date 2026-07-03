from summarizer import summarize_paper
from qa import answer_question
from citation import format_citations
from comparision import compare_papers
from paper_extractor import extract_papers
from paper_classifier import classify_paper

# ==========================================================
# Detect User Intent
# ==========================================================

def detect_intent(question):

    question = question.lower()

    summary_keywords = [
        "summary",
        "summarize",
        "summarise",
        "overview"
    ]

    comparison_keywords = [
        "compare",
        "comparison",
        "difference",
        "vs",
        "versus"
    ]

    if any(
        keyword in question
        for keyword in comparison_keywords
    ):
        return "comparison"

    if any(
        keyword in question
        for keyword in summary_keywords
    ):
        return "summary"

    return "qa"


# ==========================================================
# Main
# ==========================================================

def main():

    question = input(
        "Ask your question: "
    )

    intent = detect_intent(
        question
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    if intent == "summary":

        result = summarize_paper(
            question
        )

        print(
            "\n================ SUMMARY ================\n"
        )

        print(
            result["summary"]
        )

    # ======================================================
    # COMPARISON
    # ======================================================

    elif intent == "comparison":

        print(
            "\n================ COMPARISON ================\n"
        )

        # --------------------------------------------------
        # Temporary hardcoded paper names
        #
        # Next module:
        # Automatic paper extraction
        # --------------------------------------------------

        paper_a, paper_b = extract_papers(
            question
        )

        answer = compare_papers(
            question,
            paper_a,
            paper_b
        )
        print(answer)
    # ======================================================
    # QUESTION ANSWERING
    # ======================================================

    else:

        paper_name = classify_paper(
            question
        )

        result = answer_question(
            question,
            paper_name
        )

        print(
            "\n================ ANSWER ================\n"
        )

        print(
            result["answer"]
        )

        print(
            "\n========== SOURCES ==========\n"
        )

        print(
            format_citations(
                result["sources"]
            )
        )


# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    main()