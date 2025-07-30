from typing import List
from pydantic import BaseModel

class PromptQuery(BaseModel):
    prompt: str
    tags: List[str]