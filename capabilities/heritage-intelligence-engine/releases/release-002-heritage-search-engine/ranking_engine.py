from typing import Dict, List

from settings import CONTENT_WEIGHT, TITLE_WEIGHT


def calculate_relevance_score(query: str, card: Dict) -> int:
    """
    Calculate the relevance score of one Knowledge Card.

    Title matches receive more weight than content matches.

    Parameters
    ----------
    query : str
        User search query.

    card : Dict
        Knowledge Card containing title and content.

    Returns
    -------
    int
        Calculated relevance score.
    """

    query_words = query.lower().strip().split()

    title = card.get("title", "").lower()
    content = card.get("content", "").lower()

    score = 0

    for word in query_words:
        title_matches = title.count(word)
        content_matches = content.count(word)

        score += title_matches * TITLE_WEIGHT
        score += content_matches * CONTENT_WEIGHT

    return score


def rank_results(query: str, cards: List[Dict]) -> List[Dict]:
    """
    Score and rank Knowledge Cards from most relevant to least relevant.

    Parameters
    ----------
    query : str
        User search query.

    cards : List[Dict]
        Knowledge Cards to rank.

    Returns
    -------
    List[Dict]
        Ranked Knowledge Cards containing relevance scores.
    """

    ranked_results = []

    for card in cards:
        score = calculate_relevance_score(query, card)

        if score <= 0:
            continue

        ranked_card = card.copy()
        ranked_card["score"] = score

        ranked_results.append(ranked_card)

    return sorted(
        ranked_results,
        key=lambda result: result["score"],
        reverse=True,
    )