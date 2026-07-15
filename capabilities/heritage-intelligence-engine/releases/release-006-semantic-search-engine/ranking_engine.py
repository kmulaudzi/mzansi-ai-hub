from typing import Dict, List

from settings import CONTENT_WEIGHT, TITLE_WEIGHT


def calculate_relevance_score(
    query: str,
    document: Dict,
) -> int:
    """
    Calculate the keyword relevance score for one document.
    """

    query_words = query.lower().strip().split()

    title = document.get("title", "").lower()
    content = document.get("content", "").lower()

    score = 0

    for word in query_words:
        score += title.count(word) * TITLE_WEIGHT
        score += content.count(word) * CONTENT_WEIGHT

    return score


def rank_results(
    query: str,
    documents: List[Dict],
) -> List[Dict]:
    """
    Score and rank documents from most relevant to least relevant.
    """

    ranked_results = []

    for document in documents:
        score = calculate_relevance_score(
            query=query,
            document=document,
        )

        if score <= 0:
            continue

        ranked_document = document.copy()
        ranked_document["score"] = score

        ranked_results.append(ranked_document)

    return sorted(
        ranked_results,
        key=lambda result: result["score"],
        reverse=True,
    )