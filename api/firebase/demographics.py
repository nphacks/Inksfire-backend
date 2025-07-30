from typing import List
from .config import db
from google.cloud import firestore
from pydantic import BaseModel

class GenderDemographics(BaseModel):
    male: float
    female: float

class TargetDemographics(BaseModel):
    age: List[str]
    gender: GenderDemographics

def save_target_demographics_db(project_id: str, target_demographics: TargetDemographics):
    projects_ref = db.collection("projects")
    project_doc = projects_ref.document(project_id)
    
    # First remove existing recommended_tags if they exist
    project_doc.update({
        "target_demographics": firestore.DELETE_FIELD
    })
    
    # Then set the new tags
    project_doc.set({
        "target_demographics": target_demographics
    }, merge=True)
    
    return project_doc