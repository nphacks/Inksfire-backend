from .config import db

def create_prompt_db(project_id: str, prompt: str):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    
    project_doc.set({
        "prompt": prompt
    }, merge=True)
    
    return project_doc

# def get_prompt_db(project_id: str):
#     projects_ref = db.collection("projects")
#     project_doc = projects_ref.document(project_id) 
#     return project_doc