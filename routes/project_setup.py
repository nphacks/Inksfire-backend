from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from api.firebase.project import create_project_db, update_project_data_db
from utils.qloo.clean_fetch_tags_idea import clean_fetch_tags_idea
from utils.qloo.search_type import search_type_format
import uuid

router = APIRouter()

@router.get("/test-project-setup")
async def test_project_setup():
    return {"status": "connected!"}

@router.post("/create-project")
async def create_project(request: Request):
    try:
        body = await request.json()
        project_id = str(uuid.uuid4())
        project = create_project_db(project_id)
        body["project_id"] = project_id
        print('Hello starting', body)
        await update_project_fields_logic(body)
        print('Hello ending')
        return {"status_code": 200, "message": "Project created!", "project": project}
    
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

# Response example
# {
#   "project_id": "abc123",
#   "author": "John Doe",
#   "genre": "Sci-Fi"
#   name, idea, story_type, 
# }

@router.post("/update-project")
async def update_project_fields(request: Request):
    try:
        body = await request.json()

        if "project_id" not in body:
            raise KeyError("project_id")

        project_id = body.pop("project_id")

        if not body:
            raise HTTPException(status_code=400, detail="No data fields to update")

        project = update_project_data_db(project_id, body)

        return {"status_code": 200, "message": "Project updated!", "project": project}

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")
    

async def update_project_fields_logic(data):
    if "project_id" not in data:
        raise KeyError("project_id")

    project_id = data.pop("project_id")

    if not data:
        raise HTTPException(status_code=400, detail="No data fields to update")

    project = update_project_data_db(project_id, data)
    return project