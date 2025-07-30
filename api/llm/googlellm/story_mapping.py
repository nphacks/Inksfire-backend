from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

class StoryNode(BaseModel):
    id: str
    type: str  # "character", "location", "object"
    label: str

class StoryEdge(BaseModel):
    source: str
    target: str
    label: str

class StoryMapData(BaseModel):
    nodes: List[StoryNode]
    edges: List[StoryEdge]

def generate_story_map(writing: str):
    print("Entering story map update")

    prompt = (
        "You are a story mapping assistant.\n"
        "Given the writing below, identify any characters, objects, locations, or relationships.\n"
        "Update the story map accordingly:\n"
        "- Add nodes if they are not already present (character, location, object).\n"
        "- Add edges if new relationships or interactions are described.\n"
        "- Do not duplicate existing nodes or edges.\n\n"
        f"Writing:\n{writing}\n\n"
        "Return ONLY the updated story map in this JSON format:\n"
        "{'nodes': [...], 'edges': [...]}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": StoryMapData,
        },
    )

    return response.parsed