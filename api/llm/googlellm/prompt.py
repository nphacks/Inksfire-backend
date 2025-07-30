from typing import List, Optional
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API"))

class PromptList(BaseModel):
    prompts: List[str]

def generate_story_prompt(idea: str, tags: str, genre: Optional[str] = None):
    if genre == '':
        prompt = (
            f"Generate three 2–3 sentence story prompts in the {genre} genre for the idea: {idea}. "
            "Do not name any characters."
            "Tags are only for tone/style guidance with format: category -> sub-category -> content. "
            f"The tags: {tags}."
            "Return as: PromptList(prompts=['...', '...', '...'])"
        )
    else:
        prompt = (
            f"Generate three 2–3 sentence story prompts in any genre for the idea: {idea}. "
            "Genres: 'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western"
            "Do not name any characters."
            "Tags are only for tone/style guidance with format: category -> sub-category -> content. "
            f"The tags: {tags}."
            "Return as: PromptList(prompts=['...', '...', '...'])"
        )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": PromptList,
        },
    )

    return response.parsed