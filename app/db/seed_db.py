import asyncio

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.core import logger
from app.models.place import Place
from app.models.place_type import PlaceType
from app.models.tag import Tag


places_types = [
    {"label_pt": "Restaurante", "key": "restaurant"},
    {"label_pt": "Bar", "key": "bar"},
    {"label_pt": "Café", "key": "cafe"},
    {"label_pt": "Cinema", "key": "movie_theater"},
    {"label_pt": "Teatro", "key": "theater"},
    {"label_pt": "Parque", "key": "park"},
    {"label_pt": "Show", "key": "concert"},
    {"label_pt": "Exposição de Arte", "key": "art_gallery"},
]

tags_data = [
    {"label_pt": "Música ao Vivo", "key": "musica-ao-vivo"},
    {"label_pt": "Pet Friendly", "key": "pet-friendly"},
    {"label_pt": "Ambiente Familiar", "key": "ambiente-familiar"},
    {"label_pt": "Ar Livre", "key": "ar-livre"},
    {"label_pt": "Romântico", "key": "romantico"},
    {"label_pt": "Bom para Grupos", "key": "bom-para-grupos"},
]

place_data = [
    {
        "label": "Amicci Anchieta",
        "city": "São José dos Campos",
        "address": "Av. Anchieta, 342 - Jardim Esplanada",
        "description": "Cafeteria e confeitaria charmosa, ideal para um café da tarde ou um brunch.",
        "place_type_slugs": ["cafe"],
        "tag_slugs": ["ambiente-familiar", 'romantico']
    },
]

async def seed_db():
    logger.info("Iniciando inserções no banco de dados")
    async with AsyncSessionLocal() as db:
        logger.info("registrando place_types")
        for i in places_types:
            new_place_type = PlaceType(**i)
            db.add(new_place_type)
        await db.commit()

        logger.info("registrando tags")
        for i in tags_data:
            new_tag = Tag(**i)
            db.add(new_tag)
        await db.commit()

        for i in place_data:
            place_type_slugs = i.pop('place_type_slugs')
            tag_slugs = i.pop('tag_slugs')
            new_place = Place(**i)

            place_types = await db.execute(select(PlaceType).filter(PlaceType.key.in_(place_type_slugs)))
            place_types = place_types.scalars().all()

            tags = await db.execute(select(Tag).filter(Tag.key.in_(tag_slugs)))
            tags = tags.scalars().all()

            new_place.tags.extend(tags)
            new_place.place_types.extend(place_types)

            db.add(new_place)
        await db.commit()

        

if __name__ == "__main__":
    asyncio.run(seed_db())
    