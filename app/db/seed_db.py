import asyncio
from app.db.seed_data import categories, google_types_keys
from app.db.session import AsyncSessionLocal
from app.core import logger
from app.models import Category, GoogleType
from app.models.place_type import PlaceType


async def seed_place_categories():
    logger.info("Iniciando inserção de categorias no banco de dados.")
    async with AsyncSessionLocal() as db:
        for category in categories:
            place_type_data = category.pop("place_types")
            place_types = []
            for place_type in place_type_data:
                google_types = place_type.pop("google_types", None)
                new_place_type = PlaceType(**place_type)

                if google_types is not None:
                    google_types = [GoogleType(**i) for i in google_types if google_types is not None]
                    new_place_type.google_types = google_types

                place_types.append(new_place_type)

            new_category = Category(**category)
            new_category.place_types = place_types
            db.add(new_category)
        await db.commit()

        for data in google_types_keys:
            new_google_type = GoogleType(**data)
            db.add(new_google_type)
        await db.commit()


async def seed_db():
    logger.info("Iniciando inserções no banco de dados")
    await seed_place_categories()


if __name__ == "__main__":
    asyncio.run(seed_db())
    