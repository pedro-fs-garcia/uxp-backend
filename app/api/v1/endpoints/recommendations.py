from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.recommendation import Place, RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import search_google_places


router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    req: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    mock_places = [
        Place(name="Restaurante Fictício 1", address="Rua Falsa, 123", rating=4.5, google_place_id="id_ficticio_1"),
        Place(name="Bar de Teste", address="Avenida Exemplo, 456", rating=4.8, google_place_id="id_ficticio_2")
    ]

    found_places = search_google_places(req)

    if not found_places:
        raise HTTPException(status_code=404, detail="Nenhum lugar encontrado com os critérios fornecidos.")
    return RecommendationResponse(places=found_places)

