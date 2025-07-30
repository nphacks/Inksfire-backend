import threading
from typing import Optional
from fastapi import APIRouter, Request, BackgroundTasks, HTTPException
from api.llm.googlellm.idea import generate_story_ideas
from api.firebase.project import get_project_db, update_project_data_db
from api.llm.googlellm.prompt import generate_story_prompt
from api.llm.googlellm.story_beats import generate_story_beats
from api.llm.googlellm.story_mapping import generate_story_map
from api.llm.googlellm.character_mapping import generate_character_mapping
from api.llm.perplexity.categorize_tag_search import categorize_tag_search
from api.qloo.qloo import qloo_call
from api.firebase.tags import fuzzy_search_tags, save_tags_db
from api.media.imagegen import generate_image_from_prompt
from utils.qloo.filter_tag_types import filter_tag_types
from utils.qloo.tag_tags import tag_tags_util
from utils.qloo.unique_tags import unique_tags
from utils.qloo.taste_tags import taste_tags_util
from utils.qloo.entity_tags import entity_tags_util
from utils.qloo.suggest_tags_payload import suggest_tags_payload
from models.tags import TagsSearchQuery
from models.prompt import PromptQuery
import asyncio

router = APIRouter()

@router.get("/test-llm-generate")
async def test_llm_generate():
    return {"status": "connected!"}

@router.get("/generate-ideas")
async def generate_ideas(genre: Optional[str] = None):
    ideas = generate_story_ideas(genre)
    return { "status_code": 200, "message": "Ideas generated!", "ideas": list(ideas) }
    # return {"status_code": 200, "message": "Ideas generated!"}

@router.get("/generate-prompt")
async def generate_prompts(project_id: str):
    project_doc = get_project_db(project_id)
    project_data = project_doc.get().to_dict()
    idea = project_data.get("idea")
    # Format selected_tags
    selected_tags = ", ".join(project_data.get("selected_tags", []))
    
    # Format genres
    genres = ", ".join(project_data.get("genres", []))
    prompts = generate_story_prompt(idea, selected_tags, genres)
    return {"status_code": 200, "message": "Prompts generated!", "prompts": list(prompts) }

@router.post("/generate-image")
async def generate_prompts(request: Request):
    body = await request.json()

    prompt = body["prompt"]
    tags = body["tags"].join(", ")
    image = generate_image_from_prompt(prompt, tags)
    return {"status_code": 200, "message": "Image generated!", "image": image }

@router.post("/create-story-beats")
async def generate_story_beats(request: Request):
    body = await request.json()

    story_beats = generate_story_beats(body["writing"], body["limit"])
    update_project_data_db(body["project_id"], { "story_beats": story_beats })
    return {"status_code": 200, "message": "Story Beats generated!", "story_beats": story_beats }

@router.post("/create-story-map")
async def generate_story_map(request: Request):
    body = await request.json()

    story_map = generate_story_map(body["writing"])
    update_project_data_db(body["project_id"], { "story_map": story_map })
    return {"status_code": 200, "message": "Story Map generated!", "story_map": story_map }

@router.post("/create-character-map")
async def generate_character_map(request: Request):
    body = await request.json()

    character_map = generate_character_mapping(body["writing"])
    update_project_data_db(body["project_id"], { "character_map": character_map })
    return {"status_code": 200, "message": "Character Map generated!", "character_map": character_map }

@router.post("/suggest-tags")
async def suggest_tags(request: TagsSearchQuery):
    try:
        payload_search_string, payload_context = suggest_tags_payload(request)

        tags_db_search = []

        if len(request.searchString.split()) < 4: 
            tags_db_search = fuzzy_search_tags(request.searchString, 85, 10)

        search_list = categorize_tag_search(payload_search_string)

        payload = payload_search_string + payload_context

        if search_list['search_type'] == ['entity', 'tag']: 
            # PERFORM tag search first
            tags_external_search = tag_tags_util(payload)
            tags_external_search = filter_tag_types(tags_external_search)
            entities_used, entity_tags = entity_tags_util(payload)
            entity_tags = filter_tag_types(entity_tags)
            combined_tags = unique_tags(tags_external_search, entity_tags)
            final_tags = unique_tags(tags_db_search, combined_tags)
            # save_tags_db(final_tags)
            threading.Thread(target=save_tags_db, args=(final_tags,), daemon=True).start()
            return {"status_code": 200, "message": "Tag suggestion success!", "data": { "search_type": "tag entity", "entities_used": entities_used, "tags": final_tags }}
        elif search_list['search_type'] == ['entity']:  
            entities_used, entity_tags = entity_tags_util(payload)
            entity_tags = filter_tag_types(entity_tags)
            final_tags = unique_tags(tags_db_search, entity_tags)
            # save_tags_db(final_tags)
            threading.Thread(target=save_tags_db, args=(final_tags,), daemon=True).start()
            return {"status_code": 200, "message": "Tag suggestion success!", "data": {  "search_type": "entity", "entities_used": entities_used, "tags": final_tags }}
        elif search_list['search_type'] == ['taste']:  
            entities_used, taste_tags = taste_tags_util(payload)
            taste_tags = filter_tag_types(taste_tags)
            final_tags = unique_tags(tags_db_search, taste_tags)
            # save_tags_db(final_tags)
            threading.Thread(target=save_tags_db, args=(final_tags,), daemon=True).start()
            return {"status_code": 200, "message": "Tag suggestion success!", "data": {  "search_type": "taste", "entities_used": entities_used, "tags": final_tags }}
        elif search_list['search_type'] == ['tag']:  
            tags_external_search = tag_tags_util(payload)
            tags_external_search = filter_tag_types(tags_external_search)
            final_tags = unique_tags(tags_external_search, tags_db_search)
            # save_tags_db(final_tags)
            threading.Thread(target=save_tags_db, args=(final_tags,), daemon=True).start()
            return {"status_code": 200, "message": "Tag suggestion success!", "data": {  "search_type": "tag", "entities_used": [], "tags": final_tags }}
        
        return {"status_code": 200, "message": "Tag suggestion success!", "data": {}}
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to suggest tags: {str(e)}")