from pydantic import BaseModel
import requests
from typing import List, Optional
from app.core.config import settings
from app.schemas.recommendation_schemas import GooglePlaceRequest
from app.services.google_place_response import GooglePlaceFields, GooglePlaceResponse


class GooglePlaceSearch:
    api_url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": GooglePlaceFields.field_mask_str(),
    }

    @classmethod
    def search_by_text(cls, req: GooglePlaceRequest) -> GooglePlaceResponse:
        payload = req.model_dump(exclude_unset=True)
        print(payload.get('textQuery'))
        try:
            resp = requests.post(cls.api_url, headers=cls.headers, json=payload)
            resp.raise_for_status()  # Lança um erro para status 4xx/5xx
            data = resp.json()
            return GooglePlaceResponse.model_validate(data)
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP ocorrido: {http_err}")
            print(f"Conteúdo da resposta: {resp.text}")
        except Exception as e:
            print(f"Erro ao processar a busca no Google Places: {e}")
        return None