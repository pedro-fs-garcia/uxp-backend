import asyncio
from app.db.session import AsyncSessionLocal
from app.models.filter_options import PlaceType, Tag


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

TAGS_DATA = [
    {"name": "Música ao Vivo", "slug": "musica-ao-vivo"},
    {"name": "Pet Friendly", "slug": "pet-friendly"},
    {"name": "Ambiente Familiar", "slug": "ambiente-familiar"},
    {"name": "Ar Livre", "slug": "ar-livre"},
    {"name": "Romântico", "slug": "romantico"},
    {"name": "Bom para Grupos", "slug": "bom-para-grupos"},
]

async def seed_db():
    async with AsyncSessionLocal() as db:
        for i in places_types:
            new_place_type = PlaceType(**i)
            db.add(new_place_type)
        await db.commit()

        for i in TAGS_DATA:
            new_tag = Tag(**i)
            db.add(new_tag)
        await db.commit()

        

if __name__ == "__main__":
    asyncio.run(seed_db())
    