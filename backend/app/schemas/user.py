from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

# shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str


# properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


# additional properties to recieve via API
class User(UserInDBBase):
    pass


# additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
