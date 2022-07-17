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
    ip_address: str
    site: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    operating_system: Optional[str] = None
    os_version: Optional[str] = None
