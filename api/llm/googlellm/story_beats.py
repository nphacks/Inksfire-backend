from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os 

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

class StoryBeats(BaseModel):
    list: List[str]

def generate_story_beats(writing: str, limit: int = 12):
    print("Entering story beats")

    prompt = (
        "You are a narrative summarizer.\n"
        f"Given the writing segment, create story beats with {limit} beats.\n"
        "- Keep the arc chronological.\n"
        "- Do NOT repeat or rephrase existing arc entries.\n"
        "- Add only meaningful events (e.g. character decisions, turning points, emotional developments).\n\n"
        f"Writing:\n{writing}\n\n"
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": StoryBeats,
        },
    )

    return response.parsed