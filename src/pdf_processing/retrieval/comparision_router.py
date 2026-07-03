SPECIFIC_KEYWORDS = [
    "architecture",
    "training",
    "methodology",
    "attention mechanism",
    "self attention",
    "multi head attention",
    "embedding",
    "tokenization",
    "loss",
    "objective",
    "encoder",
    "decoder",
    "positional encoding",
    "limitations",
    "advantages",
    "dataset",
    "results",
    "experiments",
    "evaluation"
]


def detect_comparison_type(question):

    question = question.lower()

    if "compare" not in question:
        return "broad"

    for keyword in SPECIFIC_KEYWORDS:

        if keyword in question:

            return "specific"

    return "broad"