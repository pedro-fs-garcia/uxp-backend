from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core import settings
from app.db.seed_db import seed_db
from app.db.session import create_db_if_not_exists, create_tables
from app.db.session import engine
from app.core import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup ----
    logger.info("🚀 Iniciando aplicação")

    if settings.ENVIRONMENT != "production":
        await create_db_if_not_exists()
        from app.db import base
        await create_tables()
        await seed_db()

    # ponto onde a aplicação roda
    yield

    # ---- Shutdown ----
    logger.info("🛑 Encerrando aplicação")
    if settings.ENVIRONMENT != "production":
        await engine.dispose()
    logger.stop()


app = FastAPI(
    title="UrbanXP API",
    description="Backend para o concierge inteligente de experiências e roteiros.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["*"] para liberar todas
    allow_credentials=True,
    allow_methods=["*"],    # GET, POST, PUT, DELETE...
    allow_headers=["*"],    # Content-Type, Authorization...
)

@app.exception_handler(Exception)
async def global_exception_handler(req: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {
        "name": app.title,
        "status": "ok", 
        "environment": settings.ENVIRONMENT
    }