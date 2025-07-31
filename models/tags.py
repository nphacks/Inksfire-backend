from pydantic import BaseModel
from typing import List, Optional

class TagsQuerySearchQuery(BaseModel):
    search_type: List[str]

class TagsSearchQuery(BaseModel):
    searchString: Optional[str] = None
    idea: Optional[str] = None
    genres: Optional[str] = None
    story_types: Optional[str] = None
    target_age: Optional[str] = None
    target_gender: Optional[str] = None

class EntitySearchParamater(BaseModel):
    types: Optional[List[str]] = None
    exists: Optional[List[str]] = None
    popularity: Optional[str] = None
    page: Optional[int] = None
    take: Optional[int] = None
    sort_by: Optional[str] = None

class EntitySearch(BaseModel):
    entity: str
    parameters: EntitySearchParamater

class EntitySearchQuery(BaseModel):
    api_data: List[EntitySearch]

class TasteSearchParamater(BaseModel):
    trends: Optional[List[str]] = None
    # explainability: Optional[bool] = None
    content_rating: Optional[str] = None
    external: Optional[List[str]] = None
    external_imdb: Optional[str] = None
    external_rotten_tomatoes: Optional[str] = None
    finale_year_min: Optional[str] = None
    finale_year_max: Optional[str] = None
    popularity_min: Optional[str] = None
    popularity_max: Optional[str] = None
    publication_year_min: Optional[str] = None
    publication_year_max: Optional[str] = None
    rating_min: Optional[str] = None
    rating_max: Optional[str] = None
    release_country: Optional[List[str]] = None
    release_year_min: Optional[str] = None
    release_year_max: Optional[str] = None
    release_date_min: Optional[str] = None
    release_date_max: Optional[str] = None
    diversify_by: Optional[str] = None
    diversify_take: Optional[str] = None
    offset: Optional[str] = None
    page: Optional[str] = None
    location: Optional[str] = None
    sort_by: Optional[str] = None
    take: Optional[str] = None

class TasteSearch(BaseModel):
    filter_type: str
    parameters: TasteSearchParamater

class TasteSearchQuery(BaseModel):
    api_data: List[TasteSearch]

class TagSearchQuery(BaseModel):
    query: Optional[str] = None
    parent_types: Optional[List[str]] = None
    popularity_min: Optional[str] = None
    popularity_max: Optional[str] = None
    page: Optional[str] = None
    take: Optional[str] = None