from __future__ import annotations
from typing import List, Literal, Optional, Tuple
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class GooglePlaceRequest(BaseModel):
    """
    Modelo para requisições à API Google Places Text Search.
    
    Esta classe define todos os parâmetros disponíveis para realizar buscas
    textuais na API do Google Places, permitindo filtrar e personalizar
    os resultados conforme necessário.
    
    Referência da API:
    https://developers.google.com/maps/documentation/places/web-service/text-search?hl=pt-br
    
    Attributes:
        textQuery (str): Texto de consulta para busca de lugares (obrigatório)
        includedType (Optional[str]): Tipo específico de lugar (ex: 'restaurant', 'gas_station')
        strictTypeFiltering (bool): Se True, aplica filtragem rigorosa por tipo
        languageCode (str): Código do idioma para respostas (padrão: 'pt-BR')
        locationBias (dict): Tendencia a busca a uma área geográfica específica
        locationRestriction (dict): Restringe resultados a área geográfica específica
        includePureServiceAreaBusinesses (bool): Se inclui empresas apenas por área de serviço
        minRating (Optional[int]): Nota mínima dos lugares (1-5)
        openNow (bool): Filtra apenas lugares abertos agora
        pageSize (int): Número de resultados por página (máx: 20)
        priceLevels (List): Níveis de preço a incluir na busca
        rankPreference (str): Critério de ordenação ('RELEVANCE' ou 'DISTANCE')
        pageToken (str): Token para paginação de resultados
    
    Example:
        >>> request = GooglePlaceRequest(
        ...     textQuery="restaurante italiano São Paulo",
        ...     includedType="restaurant",
        ...     minRating=4,
        ...     openNow=True
        ... )
    """
    
    # Parâmetro obrigatório - texto da consulta de busca
    textQuery: str

    # Tipo específico de lugar para filtrar (opcional)
    # Exemplos: 'restaurant', 'gas_station', 'hospital', 'tourist_attraction'
    includedType: Optional[str] = None
    
    # Define se a filtragem por tipo deve ser rigorosa
    # True: apenas lugares que correspondem exatamente ao tipo
    # False: permite lugares relacionados ao tipo
    strictTypeFiltering: bool = False

    # Código do idioma para as respostas da API
    # Padrão configurado para português brasileiro
    languageCode: str = "pt-BR"

    locationBias: Optional[dict] = None

    def set_locationBias(self, latitude:float, longitude:float, radius:int = 50000) -> dict:
        """
        Define uma preferência de localização circular para a busca.
        
        Diferente de locationRestriction, este parâmetro apenas influencia
        a relevância dos resultados, sem restringir absolutamente a área.
        
        Args:
            latitude (float): Latitude do centro do círculo
            longitude (float): Longitude do centro do círculo  
            radius (int): Raio em metros (padrão: 50km)
            
        Returns:
            dict: Estrutura de bias circular ou None se city estiver definido
            
        Example:
            >>> bias = request.locationBias(-23.5505, -46.6333, 10000)
            >>> # Retorna estrutura para círculo de 10km em São Paulo
        """
        if not latitude or not longitude: return None
        self.locationBias =  {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "radius": radius
            }
        }
    
    # Restringe os resultados a uma área geográfica específica
    # Diferente do locationBias, limita absolutamente os resultados à área
    locationRestriction: dict = None

    # Controla inclusão de empresas que operam apenas por área de serviço
    # False: retorna apenas empresas com localização física
    # True: inclui empresas que atendem por área de serviço (ex: delivery)
    includePureServiceAreaBusinesses: bool = False   #  Se definido como false, a API vai retornar apenas empresas com um local físico.
    
    # Nota mínima que os lugares devem ter para serem incluídos
    # Valores válidos: 1, 2, 3, 4, 5 (baseado no sistema de estrelas do Google)
    minRating: Optional[int] = Field(None, examples = [2, 3, 4], description="Nota mínima que deve ser considerada na busca.")

    # Filtra apenas lugares abertos no momento da consulta
    # True: apenas lugares abertos agora
    # False: apenas lugares fechados agora  
    # None: não aplica filtro de horário
    openNow: bool = None

    # Número máximo de resultados por página
    # Valor máximo permitido pela API: 20
    pageSize: int = 2

    # Lista dos níveis de preço a serem incluídos na busca
    # PRICE_LEVEL_INEXPENSIVE: $ (barato)
    # PRICE_LEVEL_MODERATE: $$ (moderado)  
    # PRICE_LEVEL_EXPENSIVE: $$$ (caro)
    # PRICE_LEVEL_VERY_EXPENSIVE: $$$$ (muito caro) - pode ser adicionado
    priceLevels: List[Literal["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE", "PRICE_LEVEL_VERY_EXPENSIVE"]] = [
        "PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE", "PRICE_LEVEL_VERY_EXPENSIVE"]
    
    # Define como os resultados devem ser ordenados
    # RELEVANCE: por relevância (padrão)
    # DISTANCE: por distância (requer locationBias ou locationRestriction)
    rankPreference: Literal["RELEVANCE", "DISTANCE"] = "RELEVANCE"

    # Token para paginação, obtido do nextPageToken da resposta anterior
    # Usado para navegar entre páginas de resultados
    pageToken: str = None

    model_config = ConfigDict(from_attributes=True)
        

class PlaceRequest(BaseModel):
    """
    Modelo para requisições de busca de lugares.
    
    Esta classe define os parâmetros para realizar buscas de lugares em uma cidade
    específica, permitindo filtrar por tipos, avaliações, preços e outros critérios.
    Integrada com FastAPI para documentação automática no Swagger.
    
    Attributes:
        city (str): Cidade onde a busca será realizada (obrigatório)
        types (Optional[List[str]]): Lista de tipos de lugares para filtrar
        primaryType (Optional[str]): Tipo principal de lugar para busca
        keywords (Optional[List[str]]): Palavras-chave para refinar a busca
        useCurrentLocation (bool): Se deve usar localização atual em vez da cidade
        currentLocation (Optional[Tuple[int, int]]): Coordenadas (latitude, longitude)
        minRating (Optional[int]): Nota mínima dos lugares (1-5)
        openNow (Optional[bool]): Filtra apenas lugares abertos agora
        priceLevels (List[str]): Níveis de preço a incluir na busca
        rankPreference (str): Critério de ordenação dos resultados
    
    Example:
        >>> request = PlaceRequest(
        ...     city="São José dos Campos",
        ...     types=["restaurant", "bar"],
        ...     keywords=["comida italiana"],
        ...     minRating=4,
        ...     openNow=True
        ... )
    """

    # Cidade onde a busca será realizada (campo obrigatório)
    city: str = Field(
        ..., 
        examples=["São José dos Campos", "São Paulo", "Rio de Janeiro"], 
        description="Nome da cidade onde a busca será realizada. Este campo é obrigatório quando useCurrentLocation é False.",
        min_length=2,
        max_length=100
    )
    
    # Lista de tipos de lugares para filtrar a busca
    placeTypes: Optional[List[str]] = Field(
        None, 
        examples=[["restaurant", "bar"], ["hospital", "pharmacy"], ["gas_station"]], 
        description="Lista de tipos de lugares conforme Google Places API (ex: 'restaurant', 'bar', 'cafe', 'hospital', 'gas_station').",
        max_length=10
    )
    
    # Tipo principal de lugar para busca mais específica
    primaryType: Optional[str] = Field(
        None,
        examples=["restaurant", "lodging", "tourist_attraction"],
        description="Tipo principal de lugar quando se quer uma busca mais focada.",
        max_length=50
    )
    
    # Define se a filtragem por tipo deve ser rigorosa
    strictTypeFiltering: bool = Field(
        False,
        description="Define se a filtragem por tipo deve ser rigorosa. True: apenas lugares que correspondem exatamente ao tipo. False: permite lugares relacionados ao tipo."
    )
    
    # Palavras-chave para refinar a busca
    keywords: Optional[List[str]] = Field(
        None, 
        examples=[["comida italiana", "música ao vivo"], ["24 horas"], ["drive-thru", "delivery"]], 
        description="Lista de palavras-chave para refinar a busca (ex: 'comida italiana', 'música ao vivo', '24 horas').",
        max_length=10
    )
    
    # Flag para usar localização atual em vez da cidade
    useCurrentLocation: bool = Field(
        False,
        description="Se True, usa as coordenadas de currentLocation em vez do nome da cidade para a busca."
    )

    # Coordenadas da localização atual (latitude, longitude)
    currentLocation: Optional[Tuple[float, float]] = Field(
        None,
        examples=[(-23.2237, -45.9009), (-23.5505, -46.6333)],
        description="Coordenadas de latitude e longitude quando useCurrentLocation é True. Formato: (latitude, longitude)."
    )

    # Nota mínima que os lugares devem ter
    minRating: Optional[int] = Field(
        None, 
        examples=[2, 3, 4, 5], 
        description="Nota mínima que deve ser considerada na busca (1-5 estrelas).",
        ge=1,
        le=5
    )
    
    # Filtro para lugares abertos no momento
    openNow: Optional[bool] = Field(
        None,
        description="Se True, retorna apenas lugares abertos agora. Se False, apenas fechados. Se None, não aplica filtro."
    )

    # Lista dos níveis de preço a serem incluídos na busca
    priceLevels: List[Literal["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE", "PRICE_LEVEL_VERY_EXPENSIVE"]] = Field(
        default=["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE", "PRICE_LEVEL_VERY_EXPENSIVE"],
        description="Níveis de preço a incluir na busca. INEXPENSIVE ($), MODERATE ($$), EXPENSIVE ($$$), VERY_EXPENSIVE ($$$$).",
        min_length=1,
        max_length=4
    )
    
    # Critério de ordenação dos resultados
    rankPreference: Literal["RELEVANCE", "DISTANCE"] = Field(
        default="RELEVANCE",
        description="Como ordenar os resultados. RELEVANCE: por relevância, DISTANCE: por distância (requer localização)."
    )

    @field_validator('keywords')
    @classmethod
    def validate_keywords(cls, v: List[str]):
        """Valida cada palavra-chave individualmente."""
        # TODO: Implement validation
        return v

    @field_validator('placeTypes')
    @classmethod
    def validate_types(cls, v: List[str]):
        """Valida cada tipo de lugar individualmente."""
        # TODO: implement validation
        return v

    @field_validator('currentLocation')
    @classmethod
    def validate_current_location(cls, v: Tuple[int]):
        """Valida as coordenadas de localização."""
        if v is not None:
            if len(v) != 2:
                raise ValueError('currentLocation deve conter exatamente 2 valores: (latitude, longitude)')
            latitude, longitude = v
            if not (-90 <= latitude <= 90):
                raise ValueError('Latitude deve estar entre -90 e 90 graus')
            if not (-180 <= longitude <= 180):
                raise ValueError('Longitude deve estar entre -180 e 180 graus')
        return v

    @model_validator(mode='after')
    @classmethod
    def validate_location_logic(cls, model:"PlaceRequest"):
        """Valida a lógica entre cidade e localização atual."""
        use_current = model.useCurrentLocation
        current_location = model.currentLocation
        city = model.city
        if use_current and not current_location:
            raise ValueError('currentLocation é obrigatório quando useCurrentLocation é True')
        if not use_current and not city:
            raise ValueError('city é obrigatório quando useCurrentLocation é False')
        return model

    @model_validator(mode='after')
    @classmethod  
    def validate_distance_ranking(cls, model:"PlaceRequest"):
        """Valida se há localização para ordenação por distância."""
        rank_preference = model.rankPreference
        use_current = model.useCurrentLocation
        current_location = model.currentLocation
        if rank_preference == 'DISTANCE' and not use_current and not current_location:
            raise ValueError('Para ordenação por DISTANCE, é necessário fornecer uma localização (useCurrentLocation=True com currentLocation)')
        return model

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "city": "São José dos Campos",
                "types": ["restaurant", "bar"],
                "primaryType": "restaurant", 
                "keywords": ["comida italiana", "música ao vivo"],
                "useCurrentLocation": False,
                "currentLocation": None,
                "minRating": 4,
                "openNow": True,
                "priceLevels": ["PRICE_LEVEL_MODERATE", "PRICE_LEVEL_EXPENSIVE"],
                "rankPreference": "RELEVANCE"
            }
        }
    )