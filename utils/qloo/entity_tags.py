from utils.qloo.fetch_tags_from_response import fetch_tags_from_entity
from qloo.entity_search import entity_search
from api.qloo.qloo import qloo_call
from api.firebase.tags import save_tags_db

def entity_tags_util(payload: str):
    urls = entity_search(payload)
    entity_responses = []
    for url in urls:
        response = qloo_call(url)
        entity_responses.extend(response.get("results", []))
    entities_used, tags = fetch_tags_from_entity(entity_responses)
    return entities_used, tags