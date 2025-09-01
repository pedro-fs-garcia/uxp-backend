from pydantic import BaseModel

class BaseSchema(BaseModel):
    model_config = {
        "orm_mode": True
    }