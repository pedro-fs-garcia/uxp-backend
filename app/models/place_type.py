from __future__ import annotations
import uuid
from sqlalchemy import UUID, Column, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import BaseModel, TimestampMixin
from app.db import TableName, PlaceTypeColumn
from app.models.relationship_tables import place_type_map


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

    places = relationship(
        TableName.Place.name,
        secondary=place_type_map,
        back_populates='place_types'
    )
