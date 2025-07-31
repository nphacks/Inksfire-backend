from typing import List, Optional
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API"))

class Tag(BaseModel):
    tag_name: str
    evaluated: bool

class Tag_Evaluation(BaseModel):
    tags: List[Tag]


def evaluate_tags(writing: str, tags: str):
    prompt = (
        f"This is a story writing done by writer: {writing}"
        f"The tags: {tags}"
        f"Evalute the writing to see if each tag is getting fulfilled or addressed and return boolean value for each of them."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Tag_Evaluation,
        },
    )

    return response.parsed