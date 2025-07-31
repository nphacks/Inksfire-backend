from pydantic import BaseModel

class CreateStoryRequest(BaseModel):
    title: str
    structure: str
    timeline: str