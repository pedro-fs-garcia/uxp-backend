import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship
from app.db import TimestampMixin, TableName, CategoryColumns
from app.db.base_class import BaseModel
from app.models.relationship_tables import place_category_map


class Category(BaseModel, TimestampMixin):
    __tablename__ = TableName.Category.value

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        name=CategoryColumns.ID.value
    )
    key = Column(
        String,
        unique = True,
        index=True,
        nullable=False,
        name=CategoryColumns.KEY.value
    )
    label_pt = Column(
        String,
        unique = True,
        nullable=False,
        name=CategoryColumns.LABEL_PT.value
    )
    description_pt = Column(
        String,
        nullable=True,
        name=CategoryColumns.DESCRIPTION_PT.value
    )
    icon_url = Column(
        String,
        nullable=True,
        name=CategoryColumns.ICON_URL.value
    )

    places = relationship(
        TableName.Place.name,
        secondary=place_category_map,
        back_populates='categories'
    )

    tags = relationship(
        TableName.Tag.name,
        back_populates='category'
    )

    place_types = relationship(
        TableName.PlaceType.name,
        back_populates='category'
    )