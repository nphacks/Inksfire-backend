from models.story import CreateStoryRequest
from .config import db

def create_story_db(project_id: str, data: CreateStoryRequest):
    from google.cloud import firestore
    import uuid

    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    story_id = str(uuid.uuid4())

    story = {
        "story_id": story_id,
        "title": data.title,
        "structure": data.structure.dict() if hasattr(data.structure, "dict") else data.structure,
        "timeline": data.timeline.dict() if hasattr(data.timeline, "dict") else data.timeline,
    }

    print("Story object:", story)

    try:
        existing_doc = project_doc.get()
    except Exception as e:
        print("Failed to get document:", e)
        raise

    if not existing_doc.exists:
        project_doc.set({
            "project_id": project_id,
            "stories": [story]
        })
    else:
        print("Document exists. Appending story.")
        try:
            doc_data = existing_doc.to_dict()
            current_stories = doc_data.get("stories", [])
            if not isinstance(current_stories, list):
                raise ValueError("'stories' field must be a list")

            current_stories.append(story)
            project_doc.update({
                "stories": current_stories
            })
        except Exception as e:
            print("Failed to update document:", e)
            raise

    try:
        return project_doc.get().to_dict()
    except Exception as e:
        print("Failed to fetch updated doc:", e)
        raise


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

    return project_doc.get().to_dict()

def update_story_metadata_db(project_id: str, story_id: str, metadata: dict):
    print(project_id, story_id)
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    doc_snapshot = project_doc.get()

    if not doc_snapshot.exists:
        raise ValueError("Project not found")

    project_data = doc_snapshot.to_dict()
    stories = project_data.get("stories", [])
    print('Right before!')
    print(metadata)
    story_found = False
    for story in stories:
        if story.get("story_id") == story_id:
            # Merge new metadata into the story
            story.update(metadata)
            story_found = True
            break

    if not story_found:
        raise ValueError("Story not found in project")

    # Save changes
    project_doc.update({"stories": stories})
    return project_doc.get().to_dict()

def get_story_metadata_db(project_id: str, story_id: str, fields: list = None):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    doc_snapshot = project_doc.get()

    if not doc_snapshot.exists:
        raise ValueError("Project not found")

    project_data = doc_snapshot.to_dict()
    stories = project_data.get("stories", [])

    for story in stories:
        if story.get("story_id") == story_id:
            if fields:
                return {field: story.get(field) for field in fields}
            return story  # Return full story if no specific fields requested

    raise ValueError("Story not found in project")
