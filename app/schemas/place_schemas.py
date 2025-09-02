from typing import List, Optional
from uuid import UUID
from app.schemas import BaseSchema
from app.schemas.place_types_schemas import PlaceTypeSchema
from app.schemas.tag_schemas import TagSchema


class PlaceSchema(BaseSchema):
    id : str | UUID
    name : str
    address : str
    city : str
    description : str | None = None
    google_place_id : str | None = None
    rating: int | None = None

    tags : Optional[List[TagSchema]] | None = None

    place_types : Optional[List[PlaceTypeSchema]] | None = None


class PlaceCreateDto(BaseSchema):
    name : str
    address : str
    city : str
    description : str | None = None
    google_place_id : str | None = None
    rating: int | None = None
    tags_slugs : List[str] | None = None
    place_types_slugs : List[str] | None = None