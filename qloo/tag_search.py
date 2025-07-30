from api.llm.perplexity.tag_search_parameters import tag_search_parameters
import urllib.parse

def tag_search(payload_context: str):
    """
    Get parameters and create API links
    """
    parameters = tag_search_parameters(payload_context)

    urls = []

    query = parameters.get("query") or ""
    parent_types = parameters.get("parent_types") or []
    popularity_min = parameters.get("popularity_min")
    popularity_max = parameters.get("popularity_max")
    page = parameters.get("page") or "1"
    take = parameters.get("take") or "10"
 
    for parent_type in parent_types:
        query_params = {
            "feature.typo_tolerance": "true",
            "filter.results.tags": "",
            "filter.parents.types": parent_type,
            "filter.popularity.min": popularity_min or "",
            "filter.popularity.max": popularity_max or "",
            "filter.query": query,
            "filter.tag.types": "",
            "page": page,
            "take": take,
        }

        query_params = {k: v for k, v in query_params.items() if v != ""}

        url = "v2/tags?" + urllib.parse.urlencode(query_params)
        urls.append(url)

    return urls