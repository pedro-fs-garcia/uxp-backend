from enum import Enum

class TableName(str, Enum):
    # principais
    Place = 'places'
    Category = 'categories'
    PlaceType = 'place_types'
    Keyword = 'keywords'
    Tag = 'tags'
    GoogleType = 'google_types'
    Atmosphere = 'atmospheres'
    User = 'users'

    # relacionamentos
    PlaceCategoryMap = "place_category_map"      # N:N → places ↔ categories
    PlaceTypeMap = "place_type_map"              # N:N → places ↔ place_types
    PlaceTagMap = "place_tag_map"                # N:N → places ↔ tags
    PlaceAtmosphereMap = "place_atmosphere_map"  # N:N → places ↔ atmospheres
    UserPlaceFavorites = "user_place_favorites"  # N:N → users ↔ places
    PlaceTypeGoogleTypeMap = "place_type_google_type_map"


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
    CATEGORY_ID = 'category_id'


class TagColumn(str, Enum):
    ID = 'id'
    LABEL_PT = 'label_pt'
    KEY = 'key'


class CategoryColumns(str, Enum):
    ID = 'id'
    KEY = 'key'
    LABEL_PT = 'label_pt'
    DESCRIPTION_PT = 'description_pt'
    ICON_URL = 'icon_url'


class GoogleTypeColumns(str, Enum):
    ID = 'id'
    KEY = 'key'
    