from sqlalchemy import UUID, Column, ForeignKey, Table
from app.db.base_class import BaseModel
from app.db import TableName, PlaceColumn, PlaceTypeColumn, CategoryColumns
from app.db.enums import GoogleTypeColumns, TagColumn

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


place_category_map = Table(
    TableName.PlaceCategoryMap.value,
    BaseModel.metadata,
    Column(
        'place_id',
        UUID(as_uuid=True),
        ForeignKey(f"{TableName.Place.value}.{PlaceColumn.ID.value}"),
        primary_key=True
    ),
    Column(
        'category_id',
        UUID(as_uuid=True),
        ForeignKey(f"{TableName.Category.value}.{CategoryColumns.ID.value}"),
        primary_key=True
    )
)


place_type_google_type_map = Table(
    TableName.PlaceTypeGoogleTypeMap.value,
    BaseModel.metadata,
    Column(
        "place_Type_id",
        UUID(as_uuid=True),
        ForeignKey(f"{TableName.PlaceType.value}.{PlaceTypeColumn.ID.value}"),
        primary_key=True
    ),
    Column(
        "google_type_id",
        UUID(as_uuid=True),
        ForeignKey(f"{TableName.GoogleType.value}.{GoogleTypeColumns.ID.value}"),
        primary_key=True
    )
)
