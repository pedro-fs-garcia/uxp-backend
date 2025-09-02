from typing import List, Optional
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    city: str = Field(..., examples=["São José dos Campos"], description="Cidade onde a busca será realizada")

    price_ranges: Optional[List[int]] = Field(None, examples=[[1, 2]], description="Faixas de preço (ex: 1 para barato, 4 para muito caro).")
    types: Optional[List[str]] = Field(None, examples=[["restaurant", "bar"]], description="Tipos de lugar (ex: 'restaurant', 'bar', 'cafe').")
    keywords: Optional[List[str]] = Field(None, examples=[["comida italiana", "música ao vivo"]], description="Palavras-chave para a busca.")
    rating: Optional[int] = Field(None, examples = [2, 3, 4], description="Nota mínima que deve ser considerada na busca.")

    class Config:
        from_attributes = True
