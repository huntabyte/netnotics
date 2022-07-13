from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import Response

from app.deps.db import get_async_session
from app.deps.request_params import parse_react_admin_params
from app.deps.users import current_user
from app.models.device import Device
from app.models.user import User
from app.schemas.device import Device as DeviceSchema
from app.schemas.device import DeviceCreate, DeviceUpdate
from app.schemas.request_params import RequestParams
from app.utils.auth import hash_password

router = APIRouter(prefix="/devices")


@router.get("", response_model=List[DeviceSchema])
async def get_devices(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    request_params: RequestParams = Depends(parse_react_admin_params(Device)),
    user: User = Depends(current_user),
) -> Any:
    total = await session.scalar(
        select(func.count(Device.id).filter(Device.user_id == user.id))
    )
    devices = (
        (
            await session.execute(
                select(Device)
                .offset(request_params.skip)
                .limit(request_params.limit)
                .order_by(request_params.order_by)
                .filter(Device.user_id == user.id)
            )
        )
        .scalars()
        .all()
    )
    response.headers[
        "Content-Range"
    ] = f"{request_params.skip}-{request_params.skip + len(devices)}/{total}"
    return devices


@router.post("", response_model=DeviceSchema, status_code=201)
async def create_device(
    device_in: DeviceCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    device = device_in.dict()
    device["hashed_password"] = hash_password(device["password"])
    del device["password"]
    device = Device(**device)
    device.user_id = user.id
    session.add(device)
    await session.commit()
    return device


@router.put("/{device_id}", response_model=DeviceSchema)
async def update_device(
    device_id: int,
    device_in: DeviceUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    device: Optional[Device] = await session.get(Device, device_id)
    if not device or device.user_id != user.id:
        raise HTTPException(404)
    update_data = device_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(device, field, value)
    session.add(device)
    await session.commit()
    return device


@router.get("/{device_id}", response_model=DeviceSchema)
async def get_device(
    device_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    device: Optional[Device] = await session.get(Device, device_id)
    if not device or device.user_id != device.id:
        raise HTTPException(404)
    return device


@router.get("/{device_id}")
async def delete_device(
    device_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Any:
    device = Optional[Device] = await session.get(Device, device_id)
    if not device or device.user_id != user.id:
        raise HTTPException(404)
    await session.delete(device)
    await session.commit()
    return {"success": True}
