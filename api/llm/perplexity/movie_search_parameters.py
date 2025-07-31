import requests, os, json
from models.movie import MovieSearchParameters

def movie_search_parameters(search_string: str):
    """
    Sonar API with perpexlity performs the following tasks:
        1. Determine parameters for movie search 
    """

    payload_system = (
        "You are an expert who will understand the user search context and determine which parameters are needed for search."
        "Always return clear, structured JSON."   
        "Classify the search into one of the two types - movie or movie-list for search_type."
        "Type 'movie' is when the search specifies an exact movie"
        "Type 'movie-list' is when the search is a list of movies."
        f"The user search: {search_string}"
        "Parameters for search are: movie, movie_list, exists, popularity, sort_by"
    )

    # Parameter query
    payload_system += (
        "If type is movie-list then identify maximum 5 strongly connected movies. Save in movie_list."
        "If type is movie then give the exact movie name. Save in movie."
    )

    # Parameter types
    # types is movie

    # Parameter exists
    payload_system += (
        "Parameter exists is to filter results by existential property check like external.imdb or external.rottentomatoes."
        "According to context choose one or more: external.imdb, external.rottentomatoes."
        "If context does not specify type then choose all."
    )

    # Parameter popularity
    payload_system += (
        "Parameter popularity is minimum value of popularity an entity must have to be output."
        "The value ranges from 0-1. Determing the value depedning on the search context."
        "If popularity is not mentioned then use 0.7."
    )

    # Parameter take
    # take 5

    # Parameter sort_by
    payload_system += (
        "Parameter sort_by is sort results by criteria."
        "According to context choose one or more: match or popularity."
        "Match is sort by most similar and popularity is by most popular."
        "If user has no preference then use match."
    )

    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {os.getenv('SONAR_API')}"}
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system", 
                "content": payload_system
            },
            {
                "role": "user", 
                "content": (
                    f"{search_string}"
                    "Please output a JSON object containing the following fields: "
                    "search_type, movie, movie_list, exists, popularity, sort_by"
                )
            }
        ],
        "web_search_options": {
            "search_context_size": "medium"
        },
        "response_format": {
           "type": "json_schema",
           "json_schema": {"schema": MovieSearchParameters.model_json_schema()},
        },
    }

    response_parameters = requests.post(url, headers=headers, json=payload).json()
    movie_parameters = json.loads(response_parameters["choices"][0]["message"]["content"])

    return movie_parameters