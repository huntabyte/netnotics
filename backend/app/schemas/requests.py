from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    name: str
    password: str
