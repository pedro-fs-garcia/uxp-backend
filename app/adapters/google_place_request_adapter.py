from app.schemas.recommendation_schemas import GooglePlaceRequest, PlaceRequest


class GooglePlaceRequestAdapter:
    """Adapta PlaceRequest para GooglePlaceRequest"""

    @staticmethod
    def adapt(request_data: PlaceRequest) -> GooglePlaceRequest:
        request_data: dict = request_data.model_dump(exclude_unset=True)
        city = request_data.pop('city', None)
        types = request_data.pop('placeTypes', None)
        primary_type = request_data.pop('primaryType', None)
        keywords = request_data.pop('keywords', None)
        use_current_location = request_data.pop('useCurrentLocation', None)
        current_location = request_data.pop('currentLocation', None)

        query_parts = [primary_type] if primary_type else []
        if types: query_parts.extend(types)
        if keywords: query_parts.extend(keywords)

        if query_parts:
            text_query = ", ".join(query_parts)
        else:
            text_query = primary_type

        if city: text_query = f"{text_query} in {city}"

        google_place_request = GooglePlaceRequest(
            textQuery = text_query,
            includedType = primary_type,
            **request_data,
        )
        if use_current_location and current_location:
            lat, lng = current_location
            google_place_request.set_locationBias(lat, lng)
        
        return google_place_request