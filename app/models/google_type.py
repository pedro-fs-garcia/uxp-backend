from uuid import uuid4
from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship
from app.db.base_class import BaseModel, TimestampMixin
from app.db.enums import GoogleTypeColumns, TableName
from app.models.relationship_tables import place_type_google_type_map


class GoogleType(BaseModel, TimestampMixin):
    __tablename__ = TableName.GoogleType.value

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default = uuid4,
        name = GoogleTypeColumns.ID.value
    )
    key = Column(
        String, 
        unique=True,
        index=True,
        nullable=False,
        name=GoogleTypeColumns.KEY.value
    )

    place_types = relationship(
        TableName.PlaceType.name,
        secondary = place_type_google_type_map,
        back_populates='google_types'
    )