from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.google_place_request_adapter import GooglePlaceRequestAdapter
from app.db.session import get_db
from app.schemas.place_schemas import PlaceSchema
from app.schemas.recommendation_schemas import PlaceRequest
from app.services.local_search import urbanxp_search
from app.services.google_search import GooglePlaceSearch


router = APIRouter()

@router.post("/", response_model=List[PlaceSchema])
async def get_recommendations(
    req: PlaceRequest,
    db: AsyncSession = Depends(get_db)
):
    print("requisição: ", req)
    found_places = await urbanxp_search(db, req)

    if not found_places:
        raise HTTPException(status_code=404, detail="Nenhum lugar encontrado com os critérios fornecidos.")
    return found_places


@router.post("/google")
async def get_google_recommendation(req: PlaceRequest):
    print(f"\nreqquisição: {req}\n")
    print(req.placeTypes)
    req = GooglePlaceRequestAdapter.adapt(req)
    res = GooglePlaceSearch.search_by_text(req)    
    print("res: ", res)
    return JSONResponse(content = res.model_dump(exclude_none=True))
