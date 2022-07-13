from typing import Optional

from pydantic import BaseModel


class DeviceBase(BaseModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    username: Optional[str] = None


class DeviceCreate(DeviceBase):
    name: str
    password: str


class DeviceUpdate(DeviceBase):
    password: Optional[str] = None


class DeviceInDBBase(DeviceBase):
    id: int
    name: str
    user_id: int

    class Config:
        orm_mode = True


class Device(DeviceInDBBase):
    pass


class DeviceDB(Device):
    hashed_password: str
