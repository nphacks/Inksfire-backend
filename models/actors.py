from typing import List, Optional
from pydantic import BaseModel


class ActorNameSearchParameters(BaseModel):
    actor_names: List[str]
    type: str = 'urn:entity:actor'
    popularity: Optional[float] = None
    take: int = 1
    sort_by: Optional[str] = None