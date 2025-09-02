from typing import List
import googlemaps
from pydantic import BaseModel

from app.core.config import settings
from app.schemas.recommendation_schemas import RecommendationRequest


class GooglePlace(BaseModel):
    name: str
    address: str
    rating: int | float | str
    google_place_id: str


try:
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
except ValueError:
    gmaps = "test"


def search_google_places(req: RecommendationRequest) -> List[GooglePlace]:
    """
    Busca lugares usando a "Places API (New)" com base nos critérios da requisição.
    """
    query_parts = []
    if req.types: 
        query_parts.extend([t for t in req.types])
    
    if req.keywords:
        query_parts.extend(req.keywords)

    text_query = " ".join(query_parts)
    location_query = f"em {req.city}"
    final_query = f"{text_query} {location_query}"

    try:
        fields = [
            'places.id',
            'places.displayName',
            'places.formattedAddress',
            'places.rating'
        ]

        places_result = gmaps.places_text_search(
            text_query = final_query,
            fields = fields
        )

        found_places = []

        if places_result.get('status') == 'OK':
            for place_data in places_result.get('places', []):
                place = GooglePlace(
                    name=place_data.get('displayName'),
                    address=place_data.get('formattedAddress'),
                    rating=place_data.get('rating'),
                    google_place_id=place_data.get('id'),
                )
                found_places.append(place)
        return found_places
    
    except Exception as e:
        print("ocorreu um erro ao nuscar no Google Places (new)", e)
        return []
