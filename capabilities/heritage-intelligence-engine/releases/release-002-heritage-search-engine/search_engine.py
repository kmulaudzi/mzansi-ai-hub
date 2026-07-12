from typing import Dict, List

from ranking_engine import rank_results


def search_knowledge(
    query: str,
    knowledge_cards: List[Dict],
) -> List[Dict]:
    """
    Search and rank Knowledge Cards using keyword matching.

    Parameters
    ----------
    query : str
        User search query.

    knowledge_cards : List[Dict]
        Loaded Knowledge Cards.

    Returns
    -------
    List[Dict]
        Matching Knowledge Cards ranked by relevance.
    """

    clean_query = query.strip()

    if not clean_query:
        return []

    return rank_results(
        query=clean_query,
        cards=knowledge_cards,
    )