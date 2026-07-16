from typing import Dict, List

from ranking_engine import rank_results


def search_documents(
    query: str,
    documents: List[Dict],
) -> List[Dict]:
    """
    Search and rank documents using keyword matching.

    Parameters
    ----------
    query : str
        User search query.

    documents : List[Dict]
        Documents supplied by one or more providers.

    Returns
    -------
    List[Dict]
        Matching documents ranked by relevance.
    """

    clean_query = query.strip()

    if not clean_query:
        return []

    return rank_results(
        query=clean_query,
        documents=documents,
    )