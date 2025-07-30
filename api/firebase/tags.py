from .config import db
from google.cloud import firestore
from rapidfuzz import process
from google.cloud import firestore
from itertools import islice

def chunked(iterable, size):
    it = iter(iterable)
    return iter(lambda: list(islice(it, size)), [])

def save_tags_db(tag_list):
    """
    Save a list of tags to Firestore under the 'tags' collection.
    Skips if a tag already exists.
    """
    tags_ref = db.collection("tags")
    results = []
    tag_ids = [tag.get("tag_id") or tag.get("id") for tag in tag_list]

    existing_ids = set()
    for chunk in chunked(tag_ids, 30):
        existing_docs = tags_ref.where(field_path="tag_id", op_string="in", value=chunk).stream()
        existing_ids.update(doc.get("tag_id") for doc in existing_docs)

    batch = db.batch()
    for tag in tag_list:
        tag_id = tag.get("tag_id") or tag.get("id")
        if tag_id in existing_ids:
            results.append({"tag_id": tag_id, "status": "skipped"})
            continue

        doc_ref = tags_ref.document(tag_id)
        batch.set(doc_ref, {
            "name": tag.get("name"),
            "type": tag.get("type"),
            "tag_id": tag_id
        })
        results.append({"tag_id": tag_id, "status": "success"})

    batch.commit()
    return results

def tag_exists(tag_name):
    """
    Check if a tag exists in db
    """
    doc = db.collection("tags").document(tag_name).get()
    return doc.exists

def get_tag_by_id(tag_id):
    """
    Return tag data if it exists in Firestore, else None.
    """
    doc = db.collection("tags").document(tag_id).get()
    return doc.to_dict() if doc.exists else None

def fetch_all_tags():
    """
    Fetch all tag documents from Firestore.
    """
    tags_ref = db.collection("tags").stream()
    return [{"name": doc.to_dict().get("name"), "tag_id": doc.id, "type": doc.to_dict().get("type")} for doc in tags_ref]


def update_tag_demographics(tag_id: str, demo_data: dict):
    """
    Update the tag document in Firestore with demographics data.
    """
    db.collection("tags").document(tag_id).update({"demographics": demo_data})

def fuzzy_search_tags(user_input, threshold=70, limit=5):
    """
    Perform fuzzy matching on tag names using RapidFuzz.
    
    :param user_input: User's search query
    :param limit: Max number of results to return
    :param threshold: Minimum similarity score (0-100)
    """
    all_tags = fetch_all_tags()
    tag_names = [tag["name"] for tag in all_tags]

    # Get best matches above a threshold
    matches = process.extract(user_input, tag_names, limit=limit, score_cutoff=threshold)

    # Map matched names back to full tag data
    matched_tags = [tag for tag in all_tags if tag["name"] in [match[0] for match in matches]]
    
    return matched_tags

def select_tags_db(project_id: str, tags: list):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    
    project_doc.set({
        "selected_tags": tags
    }, merge=True)
    
    return project_doc

def get_tag_query_db(project_id: str, entity_id: str):
    project_ref = db.collection("projects").document(project_id)
    doc = project_ref.get()
    
    if not doc.exists:
        return None
        
    recommended_tags = doc.to_dict().get("recommended_tags", [])
    
    for tag in recommended_tags:
        if tag.get("entity_id") == entity_id:
            return tag.get("demographics", {})
    
    return None

def get_selected_tags(project_id: str):
    project_ref = db.collection("projects").document(project_id)
    doc = project_ref.get()
    
    if not doc.exists:
        return None
        
    return doc.to_dict().get("selected_tags", [])