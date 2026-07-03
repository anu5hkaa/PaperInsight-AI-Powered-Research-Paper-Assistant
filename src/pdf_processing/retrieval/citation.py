def format_citations(sources):

    citations = []

    seen = set()

    for source in sources:

        paper = source["metadata"]["paper_name"].title()
        chunk = source["metadata"]["chunk_id"]

        citation = f"• {paper} (Chunk {chunk})"

        if citation not in seen:
            citations.append(citation)
            seen.add(citation)

    return "\n".join(citations)