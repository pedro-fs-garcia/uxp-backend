from enum import Enum

class TableName(str, Enum):
    # principais
    Place = 'places'
    PlaceCategory = 'place_categories'
    PlaceType = 'place_types'
    Keyword = 'keywords'
    Tag = 'tags'
    Atmosphere = 'atmospheres'
    User = 'users'

    # relacionamentos
    PlaceTypeMap = "place_type_map"              # N:N → places ↔ place_types
    PlaceCategoryMap = "place_category_map"      # N:N → places ↔ place_categories
    PlaceKeywordMap = "place_keyword_map"        # N:N → places ↔ keywords
    PlaceTagMap = "place_tag_map"                # N:N → places ↔ tags
    PlaceAtmosphereMap = "place_atmosphere_map"  # N:N → places ↔ atmospheres
    UserPlaceFavorites = "user_place_favorites"  # N:N → users ↔ places


class PlaceColumn(str, Enum):
    ID = 'id'
    LABEL = 'label'
    DESCRIPTION = 'description'
    CITY = 'city'
    ADDRESS = 'address'
    RATING = 'rating'


class PlaceTypeColumn(str, Enum):
    ID = 'id'
    KEY = 'key'
    LABEL_PT = 'label_pt'
    DESCRIPTION_PT = 'description_pt'
    ICON_URL = 'icon_url'


class TagColumn(str, Enum):
    ID = 'id'
    LABEL_PT = 'label_pt'
    KEY = 'key'