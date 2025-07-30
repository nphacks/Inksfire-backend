from typing import List, Optional
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

class Idea(BaseModel):
    idea: str
    genre: str

class Ideas(BaseModel):
    ideas: List[Idea]


def generate_story_ideas(genre: Optional[str] = None):
    if genre:
        prompt = (
            f"Generate three one-line story ideas in the {genre} genre. "
            "Each idea should be 7–12 words. "
            "Return as: idea"
        )
    else:
        prompt = (
            "Generate three one-line story ideas, each from a different genre. "
            "Choose Genres from 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western'"
            "Each idea should be 7–12 words."
            "Return as: idea"
        )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Ideas,
        },
    )


    return response.parsed