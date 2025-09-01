from typing import Dict
from fastapi import APIRouter
from app.api.v1.endpoints import auth, place_types_endpoints, recommendations, tags_endpoints
from app.core.config import settings

api_router = APIRouter()

# Inclui as rotas dos outros módulos
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(recommendations.router, prefix='/recommendations', tags=['recommendations'])
api_router.include_router(place_types_endpoints.router, prefix="/place-types", tags=['place-types'])
api_router.include_router(tags_endpoints.router, prefix="/tags", tags=['tags'])


@api_router.get('/')
async def root() -> Dict[str,str]:
    return {"status": "API - versão 1", "environment": settings.ENVIRONMENT}
