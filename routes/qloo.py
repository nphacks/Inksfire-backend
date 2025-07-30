from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from api.firebase.tags import get_tag_by_id, get_tag_query_db, update_tag_demographics
from api.qloo.qloo import qloo_call
from qloo.demographics_search import demographics_search
import uuid

router = APIRouter()

@router.get("/test-qloo")
async def test_qloo():
    return {"status": "received"}

@router.get("/get-tag-info")
async def get_tag_information(tag_id: str):
    try:
        tag_data = get_tag_by_id(tag_id)
        if not tag_data:
            raise HTTPException(status_code=404, detail="Tag not found")

        demographics = tag_data.get("demographics")
        if demographics:
            return {
                "status_code": 200,
                "message": "Tag data fetched from DB!",
                "demographics": demographics
            }

        # Demographics missing: call external services
        url = demographics_search(tag_id)
        response = qloo_call(url)

        demographics_raw = response.get("results", {}).get("demographics", [])
        if not demographics_raw:
            raise HTTPException(status_code=404, detail="No demographics found in response.")

        demo_data = demographics_raw[0].get("query", {})  # contains 'age' and 'gender'

        # Save to DB using helper
        update_tag_demographics(tag_id, demo_data)

        return {
            "status_code": 200,
            "message": "Tag demographics computed!",
            "demographics": demo_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tag demographics: {str(e)}")


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tag demographics: {str(e)}")

@router.get("/add-all-demographics")
async def get_tag_information(project_id: str, entity_id: str):
    try:    
        tag_data = get_tag_query_db(project_id, entity_id)
        if tag_data:
            return {"status_code": 200, "message": "Tag data fetched!", "demographics": tag_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tag demographics: {str(e)}")