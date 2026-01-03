from pydantic import BaseModel
from typing import List

class TeaBase(BaseModel):
    name: str
    origin: str
    email: str

class TeaCreate(TeaBase):
    pass

class Tea(TeaBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True