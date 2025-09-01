from uuid import UUID
from app.schemas import BaseSchema


class _TagBase(BaseSchema):
    name: str | None = None
    slug: str | None = None


class TagSchema(_TagBase):
    id: str | UUID


class TagCreateDto(_TagBase):
    name: str
    slug: str


class TagUpdateDto(_TagBase):
    pass