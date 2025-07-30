from typing import List
from fastapi import APIRouter, HTTPException, Request
import uuid
from api.firebase.story import create_story_db, save_story_writing_db

router = APIRouter()

@router.get("/test-story")
async def test_story():
    return {"status": "connected!"}

@router.post("/create-story")
async def create_story(request: Request):
    try:
        body = await request.json()

        if "project_id" not in body:
            raise KeyError("project_id")

        project_id = body.pop("project_id")

        project = create_story_db(project_id, request)
        return {"status_code": 200, "message": "Story created!", "project": project}
    
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")
    
@router.post("/save-story")
async def save_story(request: Request):
    try:
        body = await request.json()

        if "project_id" not in body:
            raise KeyError("project_id")

        project_id = body.pop("project_id")
        story_id = body.pop("story_id")
        story_save_type = body.pop("save_type")

        if story_save_type == 'draft':
            project = save_story_writing_db(project_id, story_id, body["writing"]) 
            return {"status_code": 200, "message": "Story saved!", "project": project}
        if story_save_type == 'save':
            project = save_story_writing_db(project_id, story_id, request) 
            # Perform story beats and demographics
            return {"status_code": 200, "message": "Story saved!", "project": project}
    
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")