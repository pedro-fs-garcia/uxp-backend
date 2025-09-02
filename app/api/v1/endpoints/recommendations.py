from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.place_schemas import PlaceSchema
from app.schemas.recommendation_schemas import RecommendationRequest
from app.services.local_search import urbanxp_search
from app.services.recommendation_service import search_google_places


router = APIRouter()

@router.post("/", response_model=List[PlaceSchema])
async def get_recommendations(
    req: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    print("requisição: ", req)
    found_places = await urbanxp_search(db, req)

    if not found_places:
        raise HTTPException(status_code=404, detail="Nenhum lugar encontrado com os critérios fornecidos.")
    return found_places


@router.post("/google")
async def get_google_recommendation(
    req: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    print(f"\nreqquisição: {req}\n")
    found_places_from_google = await search_google_places()