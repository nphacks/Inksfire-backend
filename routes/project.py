from typing import List
from fastapi import APIRouter, Query, Request, BackgroundTasks, HTTPException
import uuid
from api.firebase.project import get_all_projects_db, get_project_db, get_project_information, update_project_setting
from api.firebase.tags import get_selected_tags, get_tag_by_id, get_tag_query_db, select_tags_db
from api.firebase.demographics import save_target_demographics_db
from utils.qloo.entity_classification import classifies_entities

router = APIRouter()

@router.get("/test-project")
async def test_project():
    return {"status": "connected!"}

@router.post("/get-all-projects")
async def get_all_projects(request: Request):
    try:
        body = await request.json()
        
        # If word search is made
        # If tags are selected

        projects = get_all_projects_db()
        return {"status_code": 200, "message": "Projects fetched!", "projects": projects}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")

@router.get("/get-project")
async def get_project_data(project_id: str):
    try:
        project_doc = get_project_db(project_id)
        if not project_doc.get().exists:
            raise HTTPException(status_code=404, detail="Project not found")
            
        project_data = project_doc.get().to_dict()
        
        return {
            "status_code": 200,
            "message": "Project data fetched!",
            "project": {
                "project_id": project_id,
                "name": project_data.get("name"),
                "author": project_data.get("author"),
                "genres": project_data.get("genres", []),
                "idea": project_data.get("idea"),
                "selected_tags": project_data.get("selected_tags", []),
                "story_types": project_data.get("story_types", []),
                "stories": project_data.get("stories", []),
                "target_demographics": project_data.get("target_demographics", {}),
                "project_settings": project_data.get("project_settings", {})
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project data: {str(e)}")
    
# Response example: GET /get-project-information?project_id=abc123&fields=name&fields=idea&fields=author

@router.get("/get-project-information")
async def get_project_information_route(project_id: str, fields: List[str] = Query(...)):
    try:
        project_data = get_project_information(project_id, fields)

        return {
            "status_code": 200,
            "message": "Requested project data fetched!",
            "project_id": project_id,
            "data": project_data
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project data: {str(e)}")

