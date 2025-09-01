import asyncio

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.filter_options import PlaceType, Tag
from app.core import logger
from app.models.places import Place


places_types = [
    {"name": "Restaurante", "slug": "restaurant"},
    {"name": "Bar", "slug": "bar"},
    {"name": "Café", "slug": "cafe"},
    {"name": "Cinema", "slug": "movie_theater"},
    {"name": "Teatro", "slug": "theater"},
    {"name": "Parque", "slug": "park"},
    {"name": "Show", "slug": "concert"},
    {"name": "Exposição de Arte", "slug": "art_gallery"},
]

tags_data = [
    {"name": "Música ao Vivo", "slug": "musica-ao-vivo"},
    {"name": "Pet Friendly", "slug": "pet-friendly"},
    {"name": "Ambiente Familiar", "slug": "ambiente-familiar"},
    {"name": "Ar Livre", "slug": "ar-livre"},
    {"name": "Romântico", "slug": "romantico"},
    {"name": "Bom para Grupos", "slug": "bom-para-grupos"},
]

place_data = [
    {
        "name": "Amicci Anchieta",
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

            place_types = await db.execute(select(PlaceType).filter(PlaceType.slug.in_(place_type_slugs)))
            place_types = place_types.scalars().all()

            tags = await db.execute(select(Tag).filter(Tag.slug.in_(tag_slugs)))
            tags = tags.scalars().all()

            new_place.tags.extend(tags)
            new_place.place_types.extend(place_types)

            db.add(new_place)
        await db.commit()

        

if __name__ == "__main__":
    asyncio.run(seed_db())
    