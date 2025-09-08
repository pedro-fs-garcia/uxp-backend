from uuid import UUID
from app.schemas import BaseSchema


class _PlaceTypeBase(BaseSchema):
    key: str | None = None
    label_pt: str | None = None
    description_pt: str | None = None
    icon_url: str | None = None


class PlaceTypeSchema(_PlaceTypeBase):
    id: str | UUID


class PlaceTypeCreateDto(_PlaceTypeBase):
    label_pt: str
    key: str


class PlaceTypeUpdateDto(_PlaceTypeBase):
    pass

