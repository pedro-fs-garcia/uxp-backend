from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="UrbanXP API",
    description="Backend para o concierge inteligente de experiências e roteiros.",
    version="0.1.0"
)


@app.exception_handler(Exception)
async def global_exception_handler(req: Request, exc: Exception):

    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


# Inclui o router principal da API com o prefixo /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {
        "name": app.title,
        "status": "ok", 
        "environment": settings.ENVIRONMENT
    }