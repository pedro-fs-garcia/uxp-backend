import asyncio
from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base_class import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Função de dependência para obter uma sessão de banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_db_if_not_exists():
    for _ in range(10):
        try:
            engine = create_async_engine(settings.DATABASE_SERVER_URL, isolation_level="AUTOCOMMIT")
            print('created_engine')
            async with engine.connect() as conn:
                db_name = settings.POSTGRES_DB
                result = await conn.execute(
                    text('SELECT 1 FROM pg_database WHERE datname=:name'),
                    {"name": db_name}
                )
                if not result.scalar():
                    await conn.execute(text(f'CREATE DATABASE "{db_name}" OWNER {settings.POSTGRES_USER}'))
            return
        except Exception as e:
            print(e)
            await asyncio.sleep(1)


async def create_tables():
    print(Base.metadata.tables.keys())
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print("tabelas criadas com sucesso")
    except Exception as e:
        print(e)