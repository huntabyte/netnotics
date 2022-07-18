from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr


class BaseResponse(BaseModel):
    # may define additional fields or config shared across responses
    class Config:
        orm_mode = True


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class UserResponse(BaseResponse):
    id: uuid.UUID
    email: EmailStr
    name: str


class DeviceResponse(BaseResponse):
    id: int
    name: str
    ip_address: Optional[str] = None
    fqdn: Optional[str] = None
    user_id: uuid.UUID
    site: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    operating_system: Optional[str] = None
    os_version: Optional[str] = None


class SessionResponse(BaseResponse):
    authenticated: bool
    user_id: Optional[uuid.UUID] = None
    user: Optional[UserResponse] = None
