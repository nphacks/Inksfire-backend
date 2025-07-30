import requests, os, json, re
from pydantic import BaseModel
from typing import List, Dict, Any
from models.tags import EntitySearchQuery, TagsSearchQuery

def entity_search_parameters(payload_context: str):
    """
    Sonar API with perpexlity performs the following tasks:
        1. Determine parameters for entity search 
    """

    payload_system = (
        "You are an expert who will understand the user search context and determine the parameters needed for the entity search."
        "Always return clear, structured JSON."   
        "An entity in the Qloo ecosystem represents notable people, places, things, and interests."
        "Entity search is essential for discovering and retrieving information about notable people, places, things, and interests within a system like Qloo."
        "Parameters for entity search are: query, types, exists, popularity, page, take, sort_by"
    )

    # Parameter query
    payload_system += (
        "Parameter query is a simple text to search against."
        "Identify maximum 3 strong text entities, (can be phrases or single words) to search entities for."
        "Query can be names, moods, genres, interests etc. Consider both search instructions and context to identify best entities. Unless asked specifically in search instructions, try using all of these."
        "Write parameters for each entity in parameters."
    )

    # Parameter types
    payload_system += (
        "Parameter types is a list of entity types to search for."
        "According to context choose one or more: urn:entity:movie, urn:entity:book, urn:entity:tv_show"
        "If context does not specify type then choose all."
    )

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

    # Parameter page
    payload_system += (
        "Parameter page is the page number ranging between 1-100."
        "If context gives specific sorting then determine which page to give, like top most would be page 1, and least similar world be page 100."
        "If user has no preference then use 1."
    )

    # Parameter take
    payload_system += (
        "Parameter take is number of records to return."
        "If context gives specific number then use that."
        "If user has no preference then use 3."
    )

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
                    f"{payload_context}"
                    "Please output a JSON object containing the following fields: "
                    "entity, parameters"
                )
            }
        ],
        "web_search_options": {
            "search_context_size": "low"
        },
        "response_format": {
           "type": "json_schema",
           "json_schema": {"schema": EntitySearchQuery.model_json_schema()},
        },
    }

    response_parameters = requests.post(url, headers=headers, json=payload).json()
    entity_parameters = json.loads(response_parameters["choices"][0]["message"]["content"])

    return entity_parameters