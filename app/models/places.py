import uuid
from sqlalchemy import UUID, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base


place_place_types = Table(
    'place_place_types', Base.metadata,
    Column('place_id', UUID, ForeignKey('places.id'), primary_key=True),
    Column('place_type_id', UUID, ForeignKey('place_types.id'), primary_key=True)
)

place_tags = Table(
    'place_tags', Base.metadata,
    Column('place_id', UUID, ForeignKey('places.id'), primary_key=True),
    Column('tag_id', UUID, ForeignKey('tags.id'), primary_key=True)
)


class Place (Base):
    __tablename__ = 'places'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    google_place_id = Column(String, nullable=True, unique=True)
    rating = Column(Integer, nullable=True)

    tags = relationship(
        "Tag",
        secondary = place_tags,
        back_populates = "places"
    )

    place_types = relationship(
        'PlaceType',
        secondary = place_place_types,
        back_populates='places'
    )
