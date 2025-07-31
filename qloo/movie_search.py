import urllib.parse
from api.llm.perplexity.movie_search_parameters import movie_search_parameters

def movie_search(search_str: str):
    """
    Get parameters and create API links
    """
    parameters = movie_search_parameters(search_str)

    # print("Parsed Parameters:", parameters)

    base_url = "search?"
    urls = []

    search_type = parameters.get("search_type", '')
    movie = parameters.get("movie", '')
    movie_list = parameters.get("movie_list", [])
    type = parameters.get("type", 'urn:entity:movie')
    exists = parameters.get("exists")
    popularity = parameters.get("popularity")
    sort_by = parameters.get("sort_by")

    movies = []

    if movie_list:
        movies = movie_list
    else:
        movies = [movie]

    for m in movies:
        query_params = {
            "query": m,
            "filter.type": 'urn:entity:movie',
            "take": 3
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
