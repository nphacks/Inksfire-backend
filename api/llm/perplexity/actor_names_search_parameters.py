import requests, os, json
from models.actors import ActorNameSearchParameters

def actor_names_search_parameters(search_string: str):
    """
    Sonar API with perpexlity performs the following tasks:
        1. Determine parameters for actor search 
    """

    payload_system = (
        "You are an expert who will understand the user search context and determine which parameters are needed for search."
        "Always return clear, structured JSON."   
        "User is looking for actors according to their need. Search for the best actors fiting the search query."
        f"The user search: {search_string}"
        "Parameters for search are: actor_names, popularity, sort_by"
    )

    # Parameter query
    payload_system += (
        "Identify a list of actors according to the search and save the names in actor_names."
        "Maximum give 5 names, unless user search specifies how many they want."
    )

    # Parameter types
    # types is actor

    # Parameter popularity
    payload_system += (
        "Parameter popularity is minimum value of popularity an entity must have to be output."
        "The value ranges from 0-1. Determing the value depedning on the search context."
        "If popularity is not mentioned then use 0.7."
    )

    # Parameter take
    # take 1

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
           "json_schema": {"schema": ActorNameSearchParameters.model_json_schema()},
        },
    }

    response_parameters = requests.post(url, headers=headers, json=payload).json()
    actor_name_parameters = json.loads(response_parameters["choices"][0]["message"]["content"])

    return actor_name_parameters