from typing import Optional
from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    name: str


class DeviceCreateRequest(BaseRequest):
    name: str
    ip_address: Optional[str] = None
    host: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    manageable: Optional[bool] = False


class DeviceUpdateRequest(DeviceCreateRequest):
    name: Optional[str] = None
