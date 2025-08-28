from typing import Dict
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import auth
from app.core.config import settings

api_router = APIRouter()

# Inclui as rotas dos outros módulos
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

@api_router.get('/')
async def root() -> Dict[str,str]:
    return {"status": "API - versão 1", "environment": settings.ENVIRONMENT}
