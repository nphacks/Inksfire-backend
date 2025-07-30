import requests, os, json, re
from pydantic import BaseModel
from typing import List, Dict, Any
from models.tags import TasteSearchQuery, TagsSearchQuery

def taste_search_parameters(payload_context: str):
    """
    Sonar API with perpexlity performs the following tasks:
        1. Determine parameters for taste search 
    """

    payload_system = (
        "You are an expert who will understand the user search context and determine which parameters are needed for the insights search."
        "Always return clear, structured JSON."   
        "Qloo\'s Insights API helps uncover the underlying factors that shape human preferences, offering cultural intelligence about how people relate to different entities like brands, artists, destinations, and more."
        "Parameters for insights search are: filter_type, trends, explainability, content_rating, external, finale_year, popularity_min, popularity_max, publication_year_min, publication_year_max, rating_min, rating_max,"
        " release_country, release_year_min, release_year_max, release_date_min, release_date_max, offset, page, location, sort_by, take"
        "All parameters are optional, unless specified. Choose the optional parameters depending on context."
        "If the parameter names have max or min, then max must be greater than min."
        "For parameters needing year, write full year like 2000 or 1972."
    )

    # Parameter type
    payload_system += (
        "Parameter filter_type is a list of entity types to search for. This is a required parameter."
        "According to context choose one or more: urn:entity:movie, urn:entity:book, urn:entity:tv_show."
        "If context does not specify type then choose all. List parameters for each of this filter_type."
    )

    # Parameter trends
    payload_system += (
        "Parameter trends is the level of impact a trending entity has on the results."
        "According to context choose one of these only: off, low, medium, or high."
    )

    # Parameter explainability
    # payload_system += (
    #     "Parameter explainability is explainability metadata for each recommendation and for the overall result set."
    #     "According to context choose one of these only: true or false."
    #     "By default keep it true."
    # )

    # Parameter content_rating
    payload_system += (
        "Parameter content_rating is filter by content ratings based on the MPAA film rating system, which determines suitability for various audiences."
        "According to context choose one or more: G, PG, PG-13, R, NC-17."
        "Save each of the value in a string list."
    )

    # Parameter external
    payload_system += (
        "Parameter external is to filter results by existential property check like external.imdb or external.rottentomatoes."
        "According to context choose one or more: imdb, rottentomatoes."
        "If context does not specify type then choose all. Save each of the value in a string list."
    )

    # Parameter external IMDB
    payload_system += (
        "Parameter external_imdb is to filter results above the imdb user rating between 0-10."
    )

    # Parameter external Rotten tomatoes
    payload_system += (
        "Parameter external_rotten_tomatoes is to filter results above the imdb user rating between 0-10."
    )

    # Parameter location
    payload_system += (
        "Parameter location is used to look for entities in a specific location."
        "The location can be a country like India or place like New York City."
    )

    # Parameter finale_year_min and finale_year_max
    payload_system += (
        "Parameter finale_year_min and finale_year_max can be used for only urn:entity:tv_show. This is the year finale was release for a tv series."
    )

    # Parameter popularity_min and popularity_max
    payload_system += (
        "Parameter popularity_min and popularity_max is for popularity percentile, is float number between 0-1."
        "If not mentioned keep popularity_min to 0.7."
    )

    # Parameter publication_year_min and publication_year_max
    payload_system += (
        "Parameter publication_year_min and publication_year_max are earliest and latest desired year of initial publication for the work. Can be used with only urn:entity:book."
    )

    # Parameter rating_min and rating_max
    payload_system += (
        "Parameter rating_min and rating_max are Qloo rating is float number between 0-5."
    )

    # Parameter release_country
    payload_system += (
        "Parameter release_country is to filter by a list of countries where a movie or TV show was originally released."
        "Save each of the value in a string list."
    )

    # Parameter release_year_min and release_year_max
    payload_system += (
        "Parameter release_year_min and release_year_max are earliest and latest desired release year."
    )

    # Parameter release_date_min and release_date_max
    payload_system += (
        "Parameter release_date_min and release_date_max are earliest and latest desired release dates."
        "Make sure to use ISO date format YYYY-MM-DD."
    )

    # Parameter offset
    payload_system += (
        "Parameter offset is the number of results to skip, starting from 0."
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
        "According to context choose one or more: affinity or distance."
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
           "json_schema": {"schema": TasteSearchQuery.model_json_schema()},
        },
    }

    response_parameters = requests.post(url, headers=headers, json=payload).json()
    taste_parameters = json.loads(response_parameters["choices"][0]["message"]["content"])

    return taste_parameters