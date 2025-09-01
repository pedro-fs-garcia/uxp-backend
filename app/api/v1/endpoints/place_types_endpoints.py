from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.filter_options import PlaceType
from app.schemas.place_types_schemas import PlaceTypeCreateDto, PlaceTypeSchema, PlaceTypeUpdateDto


router = APIRouter()


@router.get("/", response_model=List[PlaceTypeSchema])
async def get_all_place_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PlaceType).order_by(PlaceType.name))
    place_types = result.scalars().all()
    # if not place_types:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Nenhum tipo de local encontrado."
    #     )
    return place_types



@router.get("/{id}", response_model=PlaceTypeSchema)
async def get_one(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PlaceType).where(PlaceType.id == id))
    place_type = result.scalar_one_or_none()
    if not place_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de local {id} não encontrado."
        )
    return place_type


@router.post("/", response_model=PlaceTypeSchema, status_code=status.HTTP_201_CREATED)
async def create(dto: PlaceTypeCreateDto, db: AsyncSession = Depends(get_db)):
    new_place_type = PlaceType(**dto.model_dump(exclude_none=True))
    try:
        db.add(new_place_type)
        await db.commit()
        await db.refresh(new_place_type)
    except IntegrityError as e:
        await db.rollback()
        if "unique" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"PlaceType com slug '{new_place_type.slug}' já existe."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar PlaceType"
        )
    return new_place_type


@router.patch("/{id}", response_model=PlaceTypeSchema)
async def update(id:str, dto: PlaceTypeUpdateDto, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PlaceType).where(PlaceType.id == id))
    place_type = result.scalar_one_or_none()
    if not place_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PlaceType {id} nao encontrado."
        )

    update_data = dto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(place_type, key, value)
    
    try:
        await db.commit()
        await db.refresh(place_type)
    except IntegrityError as e:
        await db.rollback()
        
    return place_type


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PlaceType).where(PlaceType.id == id))
    place_type = result.scalar_one_or_none()
    if not place_type:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"PlaceType com id {id} não encontrado"
        )
    await db.delete(place_type)
    await db.commit()
    return None