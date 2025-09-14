from __future__ import annotations
import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import BaseModel, TimestampMixin
from app.db import TableName, PlaceTypeColumn
from app.db.enums import CategoryColumns
from app.models.relationship_tables import place_type_map, place_type_google_type_map


class PlaceType(BaseModel, TimestampMixin):
    """
    Modelo para Tipos de Lugares (ex: Restaurante, Bar, Cinema, Parque).
    """
    __tablename__ = TableName.PlaceType.value

    id = Column(
        UUID(as_uuid=True),
        primary_key=True, 
        index=True, 
        default=uuid.uuid4,
        name = PlaceTypeColumn.ID.value
    )
    key = Column(
        String, 
        unique=True, 
        index=True, 
        nullable=False,
        name=PlaceTypeColumn.KEY.value
    )
    label_pt = Column(
        String, 
        unique=True, 
        index=True, 
        nullable=False,
        name=PlaceTypeColumn.LABEL_PT.value
    )
    description_pt = Column(
        Text, 
        nullable=True
    )
    icon_url = Column(
        String, 
        nullable=True
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f"{TableName.Category.value}.{CategoryColumns.ID.value}"),
        nullable=True
    )

    category = relationship(
        TableName.Category.name,
        back_populates="place_types"
    )

    places = relationship(
        TableName.Place.name,
        secondary=place_type_map,
        back_populates='place_types'
    )

    google_types = relationship(
        TableName.GoogleType.name,
        secondary = place_type_google_type_map,
        back_populates='place_types'
    )