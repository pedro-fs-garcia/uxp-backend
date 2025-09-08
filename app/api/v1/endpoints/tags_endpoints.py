from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.tag import Tag
from app.schemas.tag_schemas import TagCreateDto, TagSchema, TagUpdateDto


router = APIRouter()


@router.get("/", response_model=List[TagSchema])
async def get_all(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).order_by(Tag.label_pt))
    result = result.scalars().all()
    return result


@router.get("/", response_model=TagSchema)
async def get_one(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == id))
    result = result.scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Tag de id {id} não encontrada"
        )
    return result


@router.post("/", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
async def create(dto: TagCreateDto, db: AsyncSession = Depends(get_db)):
    new_tag = Tag(**dto.model_dump(exclude_none=True))
    try:
        db.add(new_tag)
        await db.commit()
        await db.refresh(new_tag)
    except IntegrityError as e:
        await db.rollback()
        if "unique" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tag especificada já existe."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar Tag"
        )
    return new_tag


@router.patch("/{id}", response_model=TagSchema)
async def update(id: str, dto: TagUpdateDto, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Tag de id {id} não encontrado."
        )
    update_data = dto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tag, key, value)
    try:
        await db.commit()
        await db.refresh(tag)
    except Exception as e:
        await db.rollback()
    return tag


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag).where(Tag.id == id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Tag de id {id} não encontrado"
        )
    await db.delete(tag)
    await db.commit()
    return None