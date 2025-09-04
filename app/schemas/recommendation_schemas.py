from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class GooglePlaceRequest(BaseModel):
    # https://developers.google.com/maps/documentation/places/web-service/text-search?hl=pt-br#location-bias

    #  Se definido como false, a API vai retornar apenas empresas com um local físico.
    includePureServiceAreaBusinesses: bool = False  
    
    city: str = Field(..., examples=["São José dos Campos"], description="Cidade onde a busca será realizada")
    types: Optional[List[str]] = Field(None, examples=[["restaurant", "bar"]], description="Tipos de lugar (ex: 'restaurant', 'bar', 'cafe').")
    keywords: Optional[List[str]] = Field(None, examples=[["comida italiana", "música ao vivo"]], description="Palavras-chave para a busca.")
    primaryType: Optional[str] = None
    strictTypeFiltering: bool = False
    languageCode: str = "pt-BR"
    
    @property
    def locationBias(self) -> dict:
        if self.city: return None
        return {
            "circle": {
                "center": {
                    "latitude": 0,
                    "longitude": 0,
                },
                "radius": 50000
            }
        }

    minRating: Optional[int] = Field(None, examples = [2, 3, 4], description="Nota mínima que deve ser considerada na busca.")
    openNow: bool = None
    pageSize: int = 20

    priceLevels: List[str] = ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE"]
    rankPreference: Literal["RELEVANCE", "DISTANCE"] = "RELEVANCE"

    pageToken: str = None # Especifica o nextPageToken do corpo da resposta da página anterior.



    class Config:
        from_attributes = True


class GooglePlaceTypes(BaseModel):
    class Config:
        from_attributes = True