import json
from typing import List
from fastapi import APIRouter, HTTPException, Request
import uuid
from api.firebase.story import create_story_db, get_story_metadata_db, save_story_writing_db, update_story_metadata_db
from api.llm.googlellm.evaluate_demographics import evaluate_tags
from api.llm.googlellm.character_mapping import generate_character_mapping
from api.llm.googlellm.story_beats import generate_story_beats
from api.llm.googlellm.story_mapping import generate_story_map
from utils.data.projected_demographics import projected_demographics
from utils.data.serialize_pydantic_list import serialize_pydantic_list
from utils.data.get_tag_names import get_combined_tag_names, merge_evaluated_tags

from models.story import CreateStoryRequest

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
        data = CreateStoryRequest(**body)
        project = create_story_db(project_id, data)
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

        if story_save_type == 'save':
            project = save_story_writing_db(project_id, story_id, body["writing"]) 
            return {"status_code": 200, "message": "Story saved!", "project": project}
        if story_save_type == 'submit':
            project = save_story_writing_db(project_id, story_id, body["writing"]) 
            story_beats = generate_story_beats(body["writing"])
            selected_tags = get_story_metadata_db(project_id, story_id, ["selected_tags"])
            story_tags_evaluation = evaluate_tags(body["writing"], get_combined_tag_names(selected_tags))
            new_selected_tags = merge_evaluated_tags(selected_tags, story_tags_evaluation)
            print(new_selected_tags)
            projected_demographics_data = projected_demographics(new_selected_tags.get("selected_tags", []))
            character_mapping = generate_character_mapping(body["writing"])
            story_mapping = generate_story_map(body["writing"])
            print(projected_demographics_data)

            body = { 
                "story_beats": story_beats.list, 
                "selected_tags": new_selected_tags.get("selected_tags", []),
                "character_mapping": character_mapping.dict(),
                "story_mapping": story_mapping.dict(),
                "projected_demographics": projected_demographics_data
            }

            updated_project = update_story_metadata_db(project_id, story_id, body)

            return {"status_code": 200, "message": "Story saved!", "project": updated_project}
    
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")
    
@router.post("/update-story-metadata")
async def update_story_metadata(request: Request):
    try:
        body = await request.json()

        if "project_id" not in body:
            raise KeyError("project_id")
        if "story_id" not in body:
            raise KeyError("story_id")

        project_id = body.pop("project_id")
        story_id = body.pop("story_id")

        # `body` now contains only metadata fields to update
        updated_project = update_story_metadata_db(project_id, story_id, body)

        return {
            "status_code": 200,
            "message": "Story metadata updated successfully!",
            "project": updated_project
        }

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update story metadata: {str(e)}")
