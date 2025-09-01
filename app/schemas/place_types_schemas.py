from uuid import UUID
from app.schemas import BaseSchema


class _PlaceTypeBase(BaseSchema):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    icon_url: str | None = None


class PlaceTypeSchema(_PlaceTypeBase):
    id: str | UUID


class PlaceTypeCreateDto(_PlaceTypeBase):
    name: str
    slug: str


class PlaceTypeUpdateDto(_PlaceTypeBase):
    pass

