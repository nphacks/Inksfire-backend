from typing import List
import urllib.parse
from api.llm.perplexity.actor_names_search_parameters import actor_names_search_parameters

def actor_search(search_str: str):
    """
    Get parameters and create API links
    """
    parameters = actor_names_search_parameters(search_str)

    # print("Parsed Parameters:", parameters)

    base_url = "search?"
    urls = []

    actor_names = parameters.get("actor_names", [])
    exists = parameters.get("exists")
    popularity = parameters.get("popularity")
    sort_by = parameters.get("sort_by")

    for name in actor_names:
        query_params = {
            "query": name,
            "filter.type": 'urn:entity:actor',
            "take": 2
        }

        if exists:
            query_params["filter.exists"] = ",".join(exists)
        if popularity is not None:
            query_params["filter.popularity"] = popularity
        if sort_by:
            query_params["sort_by"] = sort_by

        encoded = urllib.parse.urlencode(query_params, doseq=True)
        final_url = base_url + encoded
        urls.append(final_url)

    return urls

def actor_entity_search(ids: List[str]):
    """
    Get parameters and create API links
    """

    base_url = "entities?entity_ids="
    urls = []

    for id in ids:
        final_url = base_url + id
        urls.append(final_url)

    return urls