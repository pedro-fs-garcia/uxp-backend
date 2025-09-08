from uuid import UUID
from app.schemas import BaseSchema


class _TagBase(BaseSchema):
    label_pt: str | None = None
    key: str | None = None


class TagSchema(_TagBase):
    id: str | UUID


class TagCreateDto(_TagBase):
    label_pt: str
    key: str


class TagUpdateDto(_TagBase):
    pass