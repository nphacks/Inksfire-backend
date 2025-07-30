from qloo.taste_search import taste_search
from utils.qloo.fetch_tags_from_response import fetch_tags_from_entity
from api.qloo.qloo import qloo_call
from api.firebase.tags import save_tags_db

def taste_tags_util(payload: str):
    urls = taste_search(payload)
    taste_responses = []
    for url in urls:
        response = qloo_call(url)
        taste_responses.extend(response.get("results", {}).get("entities", []))
    entities_used, tags = fetch_tags_from_entity(taste_responses)
    return entities_used, tags