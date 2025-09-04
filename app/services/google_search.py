from pydantic import BaseModel
import requests
from typing import List, Optional
from app.core.config import settings
from app.schemas.recommendation_schemas import GooglePlaceRequest


class GooglePlaceSearch:
    def __init__(self):
        self.api_url = "https://places.googleapis.com/v1/places:searchText"
        self.field_mask_str = ",".join([
            "places.id",
            "places.attributions",
            "places.name",
            "places.displayName",
            "places.generativeSummary",
            "places.formattedAddress",
            "places.location",
            # "places.currentOpeningHours",
            "places.rating",
            "places.priceLevel",
            "places.priceRange",
            "places.primaryType",
            "places.types",
            "places.parkingOptions",
            "nextPageToken",
        ])
        self.headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": settings.GOOGLE_MAPS_API_KEY,
            "X-Goog-FieldMask": self.field_mask_str,
        }


    def search_by_text(self, req: GooglePlaceRequest):
        query_parts = []
        if req.types:
            query_parts.extend(req.types)
        if req.keywords:
            query_parts.extend(req.keywords)

        text_query = " ".join(query_parts)
        final_query = f"{text_query} em {req.city}"
        payload = {
            "textQuery": final_query,
            "includedType": req.primaryType,
            "languageCode": "pt-BR"
        }
        try:
            resp = requests.post(self.api_url, headers=self.headers, json=payload)
            resp.raise_for_status()  # Lança um erro para status 4xx/5xx
            data = resp.json()
            return data
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP ocorrido: {http_err}")
            print(f"Conteúdo da resposta: {resp.text}")
        except Exception as e:
            print(f"Erro ao processar a busca no Google Places: {e}")
        return []