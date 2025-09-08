import uuid
from sqlalchemy import UUID, Column, Integer, String, Text
from sqlalchemy.orm import relationship, declared_attr
from app.db.base_class import BaseModel, TimestampMixin
from app.db import TableName, PlaceColumn
from app.models.relationship_tables import place_tag_map, place_type_map


class Place(BaseModel, TimestampMixin):
    __tablename__ = TableName.Place.value
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        default=uuid.uuid4, 
        name=PlaceColumn.ID.value
    )
    label = Column(
        String,
        index = True,
        nullable=False,
        name=PlaceColumn.LABEL.value
    )
    description = Column(
        Text,
        nullable=True,
        name=PlaceColumn.DESCRIPTION.value
    )
    city = Column(
        String,
        nullable=False,
        name=PlaceColumn.CITY.value
    )
    address = Column(
        String,
        nullable=False,
        name=PlaceColumn.ADDRESS.value
    )
    rating = Column(
        Integer,
        nullable=True,
        name = PlaceColumn.RATING.value
    )

    @declared_attr
    def place_types(cls):
        return relationship(
            TableName.PlaceType.name,
            secondary = place_type_map,
            back_populates = "places"
        )

    @declared_attr
    def tags(cls):
        return relationship(
            TableName.Tag.name,
            secondary=place_tag_map,
            back_populates="places"
        )
