from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.filter_options import PlaceType, Tag
from app.models.places import Place
from app.schemas.recommendation import RecommendationRequest

async def urbanxp_search(db: AsyncSession, criteria:RecommendationRequest) -> List[Place]:
    query = select(Place).options(
        selectinload(Place.place_types),
        selectinload(Place.tags)
    )
    query = query.where(Place.city.ilike(f"%{criteria.city}%"))

    if criteria.types:
        query = query.join(Place.place_types).where(PlaceType.slug.in_(criteria.types)).distinct()
    if criteria.keywords:
        query = query.join(Place.tags).where(Tag.slug.in_(criteria.keywords)).distinct()
    result = await db.execute(query)
    result = result.scalars().all()
    return result