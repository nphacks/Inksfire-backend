from typing import List, Optional

from pydantic import BaseModel


class MovieSearchParameters(BaseModel):
    search_type: str
    movie: Optional[str] = None
    movie_list: Optional[List[str]] = None
    type: str = 'urn:entity:movie'
    exists: Optional[List[str]] = None
    popularity: Optional[float] = None
    take: int = 2
    sort_by: Optional[str] = None