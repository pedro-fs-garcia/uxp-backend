from pydantic import BaseModel, EmailStr
from typing import Optional

# Propriedades compartilhadas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Propriedades para receber na criação do usuário
class UserCreate(UserBase):
    password: str

# Propriedades para receber na atualização do usuário
class UserUpdate(UserBase):
    pass

# Propriedades armazenadas no DB
class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Propriedades para retornar na API
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True