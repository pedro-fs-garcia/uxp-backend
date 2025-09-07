from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict


class GooglePlacePriceLevel(str, Enum):
    INEXPENSIVE = "PRICE_LEVEL_INEXPENSIVE"
    MODERATE = "PRICE_LEVEL_MODERATE"
    EXPENSIVE = "PRICE_LEVEL_EXPENSIVE"
    VERY_EXPENSIVE = "PRICE_LEVEL_VERY_EXPENSIVE"


class GooglePlaceDisplayName(BaseModel):
    text: Optional[str] = None
    languageCode: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlaceLocation(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlacePrice(BaseModel):
    currencyCode: Optional[str] = None
    units: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlacePriceRange(BaseModel):
    startPrice: Optional[GooglePlacePrice] = None
    endPrice: Optional[GooglePlacePrice] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlaceParkingOptions(BaseModel):
    freeParkingLot: Optional[bool] = None
    paidParkingLot: Optional[bool] = None
    valetParking: Optional[bool] = None
    streetParking: Optional[bool] = None
    freeGarageParking: Optional[bool] = None
    paidGarageParking: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)


class OpeningHourDetail(BaseModel):
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    date: Optional[Dict] = None
    model_config = ConfigDict(from_attributes=True)


class OpeningPeriod(BaseModel):
    open: Optional[OpeningHourDetail] = None
    close: Optional[OpeningHourDetail] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlaceCurrentOpeningHours(BaseModel):
    openNow: Optional[bool] = None
    periods: Optional[List[Dict]] = None
    weekdayDescriptions: Optional[List[str]] = None
    nextCloseTime: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlaceFields(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    displayName: Optional[GooglePlaceDisplayName] = None
    location: Optional[GooglePlaceLocation] = None
    formattedAddress: Optional[str] = None
    nationalPhoneNumber: Optional[str] = None
    primaryType: Optional[str] = None
    types: Optional[List[str]] = None
    rating: Optional[float] = None
    priceLevel: Optional[GooglePlacePriceLevel] = None
    priceRange: Optional[GooglePlacePriceRange] = None
    paymentOptions: Optional[Any] = None
    websiteUri: Optional[str] = None
    parkingOptions: Optional[GooglePlaceParkingOptions] = None
    attributions: Optional[List[str]] = None
    generativeSummary: Optional[str] = None
    regularOpeningHours: Optional[GooglePlaceCurrentOpeningHours] = None
    # currentOpeningHours: Optional[GooglePlaceCurrentOpeningHours] = None
    # photos: Optional[Any] = None
    businessStatus: Optional[Any]= None
    containingPlaces: Optional[Any]= None
    # googleMapsUri: Optional[Any]= None
    # googleMapsLinks: Optional[Any]= None
    subDestinations: Optional[Any]= None

    # TODO: Modelagem do addressDescriptor = None
    # addressDescriptor: Optional[Dict]  = None

    allowsDogs: Optional[bool] = None
    curbsidePickup: Optional[bool] = None
    delivery: Optional[Any] = None
    dineIn: Optional[bool] = None
    editorialSummary: Optional[Any] = None
    goodForChildren: Optional[bool] = None
    goodForGroups: Optional[bool] = None
    goodForWatchingSports: Optional[bool] = None
    liveMusic: Optional[bool] = None
    menuForChildren: Optional[bool] = None
    neighborhoodSummary: Optional[Any] = None
    
    outdoorSeating: Optional[bool] = None
    reservable: Optional[bool] = None
    restroom: Optional[bool] = None
    # reviews: Optional[Any] = None
    # reviewSummary: Optional[Any] = None

    servesBeer: Optional[bool] = None
    servesBreakfast: Optional[bool] = None
    servesBrunch: Optional[bool] = None
    servesCocktails: Optional[bool] = None
    servesCoffee: Optional[bool] = None
    servesDessert: Optional[bool] = None
    servesDinner: Optional[bool] = None
    servesLunch: Optional[bool] = None
    servesVegetarianFood: Optional[bool] = None
    servesWine: Optional[bool] = None
    takeout: Optional[bool] = None

    @classmethod
    def field_mask_str(cls) -> str:
        """Gera o fieldMask no formato places.xxx"""
        fields = []
        for field in cls.model_fields.keys():
            fields.append(f"places.{field}")
        return ",".join(fields)

    model_config = ConfigDict(from_attributes=True)


class GooglePlaceResponse(BaseModel):
    places: Optional[List[GooglePlaceFields]] = None
    nextPageToken: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class GooglePlaceType(str, Enum):
    RESTAURANT = "restaurant"
    BOWLING = "bowling_alley"
    CASINO = "casino"
    COMMEDY_CLUB = "commedy_club"
    CULTURAL_CENTER = "cultural_center"
    EVENT_VENUE = "event_venue"
    KARAOKE = "karaoke"
    MOVIE_THEATER = "movie_theater"
    NIGHT_CLUB = "night_club"
    PARK = "park"
    WATER_PARK = "water_park"
    ZOO = "zoo"
    BAR = "bar"
    CAFE = "cafe"
    PIZZARIA = "pizza_restaurant"
    ICE_CREAM = "ice_cream_shop"


# --- Categoria: Restaurantes, comida e bebida ---
FOOD_AND_DRINK = [
    "acai_shop",
    "afghani_restaurant",
    "african_restaurant",
    "american_restaurant",
    "asian_restaurant",
    "bagel_shop",
    "bakery",
    "bar",
    "bar_and_grill",
    "barbecue_restaurant",
    "brazilian_restaurant",
    "breakfast_restaurant",
    "brunch_restaurant",
    "buffet_restaurant",
    "cafe",
    "cafeteria",
    "candy_store",
    "cat_cafe",
    "chinese_restaurant",
    "chocolate_factory",
    "chocolate_shop",
    "coffee_shop",
    "confectionery",
    "deli",
    "dessert_restaurant",
    "dessert_shop",
    "diner",
    "dog_cafe",
    "donut_shop",
    "fast_food_restaurant",
    "fine_dining_restaurant",
    "food_court",
    "french_restaurant",
    "greek_restaurant",
    "hamburger_restaurant",
    "ice_cream_shop",
    "indian_restaurant",
    "indonesian_restaurant",
    "italian_restaurant",
    "japanese_restaurant",
    "juice_shop",
    "korean_restaurant",
    "lebanese_restaurant",
    "meal_delivery",
    "meal_takeaway",
    "mediterranean_restaurant",
    "mexican_restaurant",
    "middle_eastern_restaurant",
    "pizza_restaurant",
    "pub",
    "ramen_restaurant",
    "restaurant",
    "sandwich_shop",
    "seafood_restaurant",
    "spanish_restaurant",
    "steak_house",
    "sushi_restaurant",
    "tea_house",
    "thai_restaurant",
    "turkish_restaurant",
    "vegan_restaurant",
    "vegetarian_restaurant",
    "vietnamese_restaurant",
    "wine_bar"
]

# --- Categoria: Lazer, parques, entretenimento ---
LEISURE_AND_ENTERTAINMENT = [
    "adventure_sports_center",
    "amphitheatre",
    "amusement_center",
    "amusement_park",
    "aquarium",
    "banquet_hall",
    "barbecue_area",
    "botanical_garden",
    "bowling_alley",
    "casino",
    "childrens_camp",
    "comedy_club",
    "community_center",
    "concert_hall",
    "convention_center",
    "cultural_center",
    "cycling_park",
    "dance_hall",
    "dog_park",
    "event_venue",
    "ferris_wheel",
    "garden",
    "hiking_area",
    "historical_landmark",
    "internet_cafe",
    "karaoke",
    "marina",
    "movie_rental",
    "movie_theater",
    "national_park",
    "night_club",
    "observation_deck",
    "off_roading_area",
    "opera_house",
    "park",
    "philharmonic_hall",
    "picnic_ground",
    "planetarium",
    "plaza",
    "roller_coaster",
    "skateboard_park",
    "state_park",
    "tourist_attraction",
    "video_arcade",
    "visitor_center",
    "water_park",
    "wedding_venue",
    "wildlife_park",
    "wildlife_refuge",
    "zoo"
]

# --- Categoria: Cultura e artes ---
CULTURE_AND_ARTS = [
    "art_gallery",
    "art_studio",
    "auditorium",
    "cultural_landmark",
    "historical_place",
    "monument",
    "museum",
    "performing_arts_theater",
    "sculpture"
]

# --- Literal para validação com Pydantic ---
GooglePlaceType = Literal[
    *FOOD_AND_DRINK,
    *LEISURE_AND_ENTERTAINMENT,
    *CULTURE_AND_ARTS
]