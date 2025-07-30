from pydantic import BaseModel
from google.cloud import firestore
from .config import db
import uuid

class CreateStoryRequest(BaseModel):
    name: str
    structure: str
    timeline: str

def create_story_db(project_id: str, data: CreateStoryRequest):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)

    story_id = str(uuid.uuid4())
    story = {
        "story_id": story_id,
        "name": data.name,
        "structure": data.structure,
        "timeline": data.timeline
    }

    if not project_doc.get().exists:
        project_doc.set({
            "project_id": project_id,
            "stories": [story]
        })
    else:
        project_doc.update({
            "stories": firestore.ArrayUnion([story])
        })

    return project_doc

def save_story_writing_db(project_id: str, story_id: str, writing: str):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    doc_snapshot = project_doc.get()

    if not doc_snapshot.exists:
        raise ValueError("Project not found")

    data = doc_snapshot.to_dict()
    stories = data.get("stories", [])

    # Update the matching story
    updated = False
    for story in stories:
        if story.get("story_id") == story_id:
            story["writing"] = writing
            updated = True
            break

    if not updated:
        raise ValueError("Story not found in project")

    # Save the updated stories list
    project_doc.update({
        "stories": stories
    })

    return project_doc
