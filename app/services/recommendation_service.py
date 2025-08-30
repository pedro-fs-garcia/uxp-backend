# from typing import List
# import googlemaps

# from app.core.config import settings
# from app.schemas.recommendation import Place, RecommendationRequest


# gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

# async def search_google_places(req: RecommendationRequest) -> List[Place]:
#     """
#     Busca lugares usando a "Places API (New)" com base nos critérios da requisição.
#     """
#     query_parts = []
#     if req.types: 
#         query_parts.extend([t.replace('restaurantes', 'reastaurant').replace('bares', 'bars') for t in req.types])
    

#     if req.keywords:
#         query_parts.extend(req.keywords)

#     text_query = " ".join(query_parts)
#     location_query = f"em {req.city}"
#     final_query = f"{text_query} {location_query}"

#     try:
#         fields = [
#             'places.id',
#             'places.displayName',
#             'places.formattedAddress',
#             'places.rating'
#         ]

#         places_result = gmaps.places_text_search(
#             query = final_query,
#             fields = fields
#         )

#         found_places = []

#         if places_result.get('status') == 'OK':
#             for place_data in places_result.get('places', []):
#                 place = Place(
#                     name=place_data.get('displayName'),
#                     address=place_data.get('formattedAddress'),
#                     rating=place_data.get('rating'),
#                     google_place_id=place_data.get('id'),
#                 )
#                 found_places.append(place)
#         return found_places
    
#     except Exception as e:
#         print("ocorreu um erro ao nuscar no Google Places (new)", e)
#         return []

import requests
from app.core.config import settings
from app.schemas.recommendation import RecommendationRequest, Place

# URL do endpoint "Text Search" da nova API
PLACES_API_URL = "https://places.googleapis.com/v1/places:searchText"

# Cabeçalhos necessários para a requisição
HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
    "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating"
}

# Note que a função não é mais "async def", pois a biblioteca requests é síncrona
def search_google_places(request: RecommendationRequest) -> list[Place]:
    """
    Busca lugares usando uma chamada HTTP direta para a "Places API (New)".
    """
    query_parts = []
    if request.types:
        query_parts.extend([t.replace('restaurantes', 'restaurant').replace('bares', 'bar') for t in request.types])
    
    if request.keywords:
        query_parts.extend(request.keywords)
    
    text_query = " ".join(query_parts)
    final_query = f"{text_query} em {request.city}"
    
    print(f"Executando busca direta na Places API (New) com a query: '{final_query}'")

    # Corpo da requisição em formato JSON
    payload = {
        "textQuery": final_query,
        "languageCode": "pt-BR", # Definimos o idioma aqui
    }

    try:
        # A chamada HTTP POST usando a biblioteca requests
        response = requests.post(PLACES_API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()  # Lança um erro se a resposta for 4xx ou 5xx
        
        response_data = response.json()
        found_places = []
        
        for place_data in response_data.get('places', []):
            place = Place(
                name=place_data.get('displayName'),
                address=place_data.get('formattedAddress'),
                rating=place_data.get('rating'),
                google_place_id=place_data.get('id')
            )
            found_places.append(place)
            
        return found_places

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ocorrido: {http_err}")
        print(f"Conteúdo da resposta: {response.text}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro ao buscar no Google Places (New): {e}")
        return []