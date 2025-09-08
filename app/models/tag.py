from __future__ import annotations
import uuid
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship
from app.db.base_class import BaseModel, TimestampMixin
from app.db import TableName
from app.db.enums import TagColumn
from app.models.relationship_tables import place_tag_map


class Tag(BaseModel, TimestampMixin):
    """
    Modelo para Palavras-chave/Tags (ex: música-ao-vivo, pet-friendly).
    """
    __tablename__ = TableName.Tag.value

    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        index=True, 
        default=uuid.uuid4, 
        name=TagColumn.ID.value
    )
    label_pt = Column(
        String, 
        unique=True, 
        index=True, 
        nullable=False
    )
    key = Column(
        String, 
        unique=True, 
        index=True, 
        nullable=False
    )

    places = relationship(
        TableName.Place.name,
        secondary = place_tag_map,
        back_populates='tags'
    )

