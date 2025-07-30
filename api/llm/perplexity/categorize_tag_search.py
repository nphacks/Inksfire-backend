import requests, os, json, re
from pydantic import BaseModel
from typing import List, Dict, Any
from models.tags import TagsQuerySearchQuery, TagsSearchQuery

def categorize_tag_search(payload_context: str):
    """
    Sonar API with perpexlity performs the following tasks:
        1. Read the context of search query: the user search, story idea, genre, type and 
        target demographics to determine the type of search to perform - tag, entity, insights or combination
    """

    payload_system = (
        "You are an expert system that classifies open-ended user search queries into one of the allowed search types used for discovering tags in the Qloo ecosystem."
        "Allowed outputs are only: ['entity'], ['taste'], ['entity', 'tag']"
        "Never return: All three types together, ['tag'] alone, or ['entity', 'taste']"
    )

    # Definitions
    payload_system += (
        "\nDefinitions:\n"

        "Entity:\n"
        "- Represents a focused concept or subject the user is searching for.\n"
        "- Can be: A genre (e.g., 'horror', 'comedy'), A proper noun or named title (e.g., 'Inception', 'Harry Potter'), A short or long descriptive phrase or theme (e.g., 'a happy-go-lucky story')\n"
        "- Also use 'entity' if the user gives a detailed description (more than 5 words).\n\n"

        "Tag:\n"
        "- Represents a subcategory or conceptual theme associated with entities.\n"
        "- These are short (max 4-5 words) phrases like: 'circle of life', 'father-daughter bond', 'coming of age'\n"
        "- Only use 'tag' **along with 'entity'** when the query is thematic but doesn't include any taste filters.\n"
        "- Never use 'tag' by itself and never combine 'tag' with 'taste'.\n\n"

        "Taste:\n"
        "- Used when the query contains specific filter attributes, including: content rating, external, date, year, popularity, rating, release country"
        "- Use 'taste' even if there's no 'entity' — for example: 'TV shows in 2005'\n"
        "- If any of the above attributes are mentioned, classify as ['taste'] only.\n\n"
    )

    # Classification Rules
    payload_system += (
        "\nClassification Rules:\n"

        "1. Use ['tag', 'entity'] if:\n"
        "- The query is thematic or descriptive and contains **no taste attributes**.\n"
        "- Example: 'a story about redemption', 'father-son bond in a movie'\n\n"

        "2. Use ['entity'] if:\n"
        "- The query includes a genre, a named entity, or is a long explanation (>5 words).\n"
        "- And there are no taste-related filters.\n"
        "- Example: 'a light-hearted romantic comedy set in Paris'\n\n"

        "3. Use ['taste'] if:\n"
        "- The query includes any of the defined taste attributes.\n"
        "- Example: 'TV shows from 2005', 'popular horror films with rating > 8'\n\n"

        "\n"
        "Important:\n"
        "\n"
        "- Never return all three types.\n"
        "- Never classify as ['tag'] alone.\n"
        "- Never combine 'tag' with 'taste'.\n"
        "- Do not invent or infer attributes that are not explicitly mentioned.\n"
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
                    "search_type"
                )
            }
        ],
        "web_search_options": {
            "search_context_size": "low"
        },
        "response_format": {
           "type": "json_schema",
           "json_schema": {"schema": TagsQuerySearchQuery.model_json_schema()},
        },
    }

    response_search = requests.post(url, headers=headers, json=payload).json()
    search_type = json.loads(response_search["choices"][0]["message"]["content"])    

    return search_type