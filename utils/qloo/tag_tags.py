from qloo.tag_search import tag_search
from api.qloo.qloo import qloo_call
from api.firebase.tags import save_tags_db

def tag_tags_util(payload: str):
    urls = tag_search(payload)
    tags = []
    for url in urls:
        response = qloo_call(url)
        tags.extend(response.get("results", {}).get("tags", []))
    
    
    return tags