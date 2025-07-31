from .config import db

def get_all_projects_db():
    projects_ref = db.collection("projects")
    docs = projects_ref.stream()
    return [{
        "project_id": doc.id,
        "name": doc.to_dict().get("name"),
        "author": doc.to_dict().get("author"),
        "idea": doc.to_dict().get("idea"),
        "genres": doc.to_dict().get("genres"),
        "story_types": doc.to_dict().get("story_types")
    } for doc in docs]

def get_project_db(project_id: str):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id) 

    if not project_doc.get().exists:
        raise ValueError("Project not found")

    return project_doc.get().to_dict()


def get_project_information(project_id: str, fields: list):
    project_doc = get_project_db(project_id)
    data = project_doc.get().to_dict()
    return {field: data.get(field) for field in fields}

def create_project_db(project_id: str):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)

    project_settings = {
        "story_beats": 'AI',
        "character_mapping": 'AI',
        "story_mapping": 'AI',
        "theme": 'theme_1'
    }
    
    if not project_doc.get().exists:
        project_doc.set({
            "project_id": project_id,
            "project_settings": project_settings
        })
    
    return project_doc.get().to_dict()

def update_project_data_db(project_id: str, data: dict):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)

    if not project_doc.get().exists:
        raise ValueError("Project does not exist")

    project_doc.update(data)

    return project_doc.get().to_dict()

def update_project_setting(project_id: str, setting_key: str, setting_value: str):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    
    if not project_doc.get().exists:
        raise ValueError("Project does not exist")
    
    valid_settings = ["story_beats", "character_mapping", "story_mapping", "theme"]
    
    if setting_key not in valid_settings:
        raise ValueError(f"Invalid setting key. Must be one of: {valid_settings}")
    
    project_doc.update({
        f"project_settings.{setting_key}": setting_value
    })
    
    return project_doc.get().to_dict()
