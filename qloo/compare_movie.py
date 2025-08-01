from typing import List
import urllib.parse
from api.llm.perplexity.movie_search_parameters import movie_search_parameters

def compare_movie_search(entity_ids: List[str]):
    """
    Get parameters and create API links
    """
    url = f'v2/insights/compare?a.signal.interests.entities={entity_ids[0]}&b.signal.interests.entities={entity_ids[1]}&model=descriptive&page=1&take=20'

    return url