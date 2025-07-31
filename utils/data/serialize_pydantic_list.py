from typing import List
from pydantic import BaseModel

def serialize_pydantic_list(items: List[BaseModel]) -> List[dict]:
    print(items)
    return [item.dict() for item in items]
