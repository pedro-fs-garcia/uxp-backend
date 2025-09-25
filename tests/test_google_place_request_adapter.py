import pytest
from app.adapters.google_place_request_adapter import GooglePlaceRequestAdapter
from app.schemas.recommendation_schemas import PlaceRequest, GooglePlaceRequest

# Python

class DummyGooglePlaceRequest(GooglePlaceRequest):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locationBias = None
    def set_locationBias(self, lat, lng):
        self.locationBias = {'latitude': lat, 'longitude': lng}

@pytest.fixture(autouse=True)
def patch_google_place_request(monkeypatch):
    monkeypatch.setattr(
        "app.schemas.recommendation_schemas.GooglePlaceRequest",
        DummyGooglePlaceRequest
    )

def test_adapt_all_fields():
    req = PlaceRequest(
        city="São Paulo",
        placeTypes=["restaurant", "bar"],
        primaryType="food",
        keywords=["pizza", "happy hour"],
        useCurrentLocation=True,
        currentLocation=(10.0, 20.0),
        minRating=4,
        openNow=True,
        priceLevels=["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE"],
        rankPreference="RELEVANCE"
    )
    result = GooglePlaceRequestAdapter.adapt(req)
    assert result.textQuery == "food, restaurant, bar, pizza, happy hour in São Paulo"
    assert result.includedType == "food"
    assert result.locationBias == {"circle": {"center":{'latitude': 10.0, 'longitude': 20.0}, "radius": 50000}}
    assert result.minRating == 4
    assert result.openNow is True
    assert result.priceLevels == ["PRICE_LEVEL_INEXPENSIVE", "PRICE_LEVEL_MODERATE"]
    assert result.rankPreference == "RELEVANCE"

def test_adapt_primary_type_and_city():
    req = PlaceRequest(
        city="Rio de Janeiro",
        primaryType="museum"
    )
    result = GooglePlaceRequestAdapter.adapt(req)
    assert result.textQuery == "museum in Rio de Janeiro"
    assert result.includedType == "museum"

def test_adapt_types_and_keywords():
    req = PlaceRequest(
        city = "São José dos Campos",
        placeTypes=["park", "garden"],
        keywords=["nature", "outdoor"]
    )
    result = GooglePlaceRequestAdapter.adapt(req)
    assert result.textQuery == "park, garden, nature, outdoor in São José dos Campos"
    assert result.includedType is None

def test_adapt_use_current_location():
    req = PlaceRequest(
        city = "Ribeirão Preto",
        primaryType="cafe",
        useCurrentLocation=True,
        currentLocation=(55.5, 44.4)
    )
    result = GooglePlaceRequestAdapter.adapt(req)
    assert result.locationBias == {"circle": {"center":{'latitude': 55.5, 'longitude': 44.4}, "radius": 50000}}

def test_adapt_minimal():
    req = PlaceRequest(city = "Salvador",  primaryType="library")
    result = GooglePlaceRequestAdapter.adapt(req)
    assert result.textQuery == "library in Salvador"
    assert result.includedType == "library"
    assert result.locationBias is None