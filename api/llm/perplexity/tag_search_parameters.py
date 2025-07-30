import requests, os, json, re
from pydantic import BaseModel
from typing import List, Dict, Any
from models.tags import TagSearchQuery

def tag_search_parameters(payload_context: str):
    """
    Sonar API with perpexlity performs the following tasks:
        1. Determine parameters for tag search 
    """

    payload_system = (
        "You are an expert who will understand the user search context and determine which parameters are needed for the tag search."
        "Always return clear, structured JSON."   
        "Tags are a type of entity in the Qloo ecosystem that serve as labels to categorize and enrich other entities."
        "Parameters for insights search are: query, parent_types, popularity_min, popularity_max, tag_types, page and take."
    )

    # Parameter query
    payload_system += (
        "Parameter query is partial string search on the tag name."
    )

    # Parameter parent_types
    payload_system += (
        "Parameter parent_types is parental entity types: urn:entity:book, urn:entity:tv_show and urn:entity:movie."
        "Use one or more and add to string list."
    )

    # Parameter popularity_min and popularity_max
    payload_system += (
        "Parameter popularity_min and popularity_max for popularity percentile, is float number between 0-1."
        "If not mentioned keep popularity_min to 0.7."
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
           "json_schema": {"schema": TagSearchQuery.model_json_schema()},
        },
    }

    response_parameters = requests.post(url, headers=headers, json=payload).json()
    tag_parameters = json.loads(response_parameters["choices"][0]["message"]["content"])

    return tag_parameters