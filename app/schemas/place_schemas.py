from typing import List
from sqlalchemy import UUID
from app.schemas import BaseSchema


class PlaceSchema(BaseSchema):
    id : str | UUID
    name : str
    address : str
    city : str
    description : str
    google_place_id : str

    tags : List

    place_types : List
