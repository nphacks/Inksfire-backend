from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from api.firebase.tags import get_tag_by_id, get_tag_query_db, update_tag_demographics
from api.qloo.qloo import qloo_call
from qloo.compare_movie import compare_movie_search
from qloo.actor_search import actor_entity_search, actor_search
from qloo.movie_search import movie_search
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

    
@router.get("/get-movie-info")
async def movie_information_search(movie_search_Str: str):
    try:
        urls = movie_search(movie_search_Str)
        movies = []

        for url in urls:
            response = qloo_call(url)
            print(response)
            movies.extend(response["results"])

        return {
            "status_code": 200,
            "message": "Movie searched!",
            "movie_information": movies
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch movie information: {str(e)}")
    
@router.get("/get-movie-compare-info")
async def movie_compare_information(entity_1: str, entity_2: str):
    try:
        print('Reaching')
        url = compare_movie_search([entity_1, entity_2])
        print(url)
        response = qloo_call(url)
        print(response)
        return {
            "status_code": 200,
            "message": "Movie compare data found!",
            "movie_compare": response["results"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch compare results: {str(e)}")
    
@router.get("/get-actor-info")
async def actor_information_search(movie_search_Str: str):
    try:
        urls = actor_search(movie_search_Str)
        actor_entities = []

        for url in urls:
            response = qloo_call(url)
            for entities in response["results"]:
                actor_entities.append(entities["entity_id"])
            
        actor_id_urls = actor_entity_search(actor_entities)
        actors = []

        for url in actor_id_urls:
            response = qloo_call(url)
            print(response)
            actors.append(response["results"][0])

        print(actors)

        return {
            "status_code": 200,
            "message": "Movie searched!",
            "actors_information": actors
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch actor information: {str(e)}")

@router.get("/add-all-demographics")
async def get_tag_information(project_id: str, entity_id: str):
    try:    
        tag_data = get_tag_query_db(project_id, entity_id)
        if tag_data:
            return {"status_code": 200, "message": "Tag data fetched!", "demographics": tag_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tag demographics: {str(e)}")