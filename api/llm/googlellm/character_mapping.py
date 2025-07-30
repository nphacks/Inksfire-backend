from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os 

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

class RelationshipStep(BaseModel):
    step: str
    type: str
    notes: str

class CharacterRelationship(BaseModel):
    source: str
    target: str
    history: List[RelationshipStep]

class CharacterMapEntry(BaseModel):
    name: str
    description: str

class CharacterMap(BaseModel):
    characters: List[CharacterMapEntry]
    relationships: List[CharacterRelationship]

def generate_character_mapping(writing: str):
    print("Entering character map update")

    prompt = (
        "You are a story analyzer.\n"
        "From the writing below, identify introduced characters and their relationships relationships.\n"
        "If there is a major update in relationship like marriage, then add an additional relationship."
        "Create character map accordingly:\n"
        "- Append characters.\n"
        "- For relationships, add new steps if found.\n"
        "- Add new relationships only if meaningful relationship change occur. Write in 1-3 words.\n\n"
        f"Writing:\n{writing}\n\n"
        "Return ONLY the updated character map in this exact JSON format:\n"
        "{'characters': [...], 'relationships': [...]}"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CharacterMap,
        },
    )

    return response.parsed