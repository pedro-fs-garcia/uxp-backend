from sqlalchemy import UUID, Column, ForeignKey, Table
from app.db.base_class import BaseModel
from app.db import TableName, PlaceColumn, PlaceTypeColumn
from app.db.enums import TagColumn


place_type_map = Table(
    TableName.PlaceTypeMap.value,
    BaseModel.metadata,
    Column(
        'place_id', 
        UUID(as_uuid=True), 
        ForeignKey(f"{TableName.Place.value}.{PlaceColumn.ID.value}"), 
        primary_key=True
    ),
    Column(
        'place_type_id', 
        UUID(as_uuid=True), 
        ForeignKey(f"{TableName.PlaceType.value}.{PlaceTypeColumn.ID.value}"), 
        primary_key=True
    )
)


place_tag_map = Table(
    TableName.PlaceTagMap.value,
    BaseModel.metadata,
    Column(
        'place_id', 
        UUID(as_uuid=True), 
        ForeignKey(f"{TableName.Place.value}.{PlaceColumn.ID.value}"), 
        primary_key=True
    ),
    Column(
        'tag_id', 
        UUID(as_uuid=True), 
        ForeignKey(f"{TableName.Tag.value}.{TagColumn.ID.value}"), 
        primary_key=True
    )
)
