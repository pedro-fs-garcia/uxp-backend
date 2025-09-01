import uuid
from sqlalchemy import UUID, Column, String, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base, TimestampMixin


class PlaceType(Base, TimestampMixin):
    """
    Modelo para Tipos de Lugares (ex: Restaurante, Bar, Cinema, Parque).
    """
    __tablename__ = 'place_types'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)

    places = relationship(
        'Place',
        secondary='place_place_types',
        back_populates='place_types'
    )


class Tag(Base, TimestampMixin):
    """
    Modelo para Palavras-chave/Tags (ex: música-ao-vivo, pet-friendly).
    """
    __tablename__ = 'tags'

    id= Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    places = relationship(
        'Place',
        secondary = 'place_tags',
        back_populates='tags'
    )