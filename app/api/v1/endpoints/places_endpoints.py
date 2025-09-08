from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.place import Place
from app.models.place_type import PlaceType
from app.models.tag import Tag
from app.schemas.place_schemas import PlaceCreateDto, PlaceSchema


router = APIRouter()

@router.get("/", response_model=List[PlaceSchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Place)
        .options(
            selectinload(Place.tags),
            selectinload(Place.place_types)
        )
        .order_by(Place.rating)
    )
    result = result.scalars().all()
    return result


@router.get("/{id}", response_model=PlaceSchema)
async def get_one(id:str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Place).where(Place.id == id))
    result = result.scalar_one_or_none()
    return result


@router.post("/", response_model=PlaceSchema, status_code=status.HTTP_201_CREATED)
async def create(dto: PlaceCreateDto, db: AsyncSession = Depends(get_db)):
    try:
        dto = dto.model_dump(exclude_none=True)
        types_slugs = dto.pop('place_type_slugs')
        tag_slugs = dto.pop('tag_slugs')
        new_place = Place(**dto)
        if types_slugs:
            place_types = await db.execute(select(PlaceType).filter(PlaceType.key.in_(types_slugs)))
            place_types = place_types.scalars().all()
            new_place.place_types.extend(place_types)
        if tag_slugs:
            place_tags = await db.execute(select(Tag).filter(Tag.key.in_(tag_slugs)))
            place_tags = place_tags.scalars().all()
            new_place.place_types.extend(place_tags)
        db.add(new_place)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar Place"
        )
    return new_place

