from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash
from app.models import Device, User
from app.schemas.requests import DeviceCreateRequest
from app.schemas.responses import DeviceResponse

router = APIRouter()


@router.post("", response_model=DeviceResponse, status_code=201)
async def create_device(
    new_device: DeviceCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Creates a new device. Only for logged in users.
    """

    try:
        if new_device.password:
            hashed_password = get_password_hash(new_device.password)
        else:
            hashed_password = None

        device = Device(
            user_id=current_user.id,
            name=new_device.name,
            ip_address=new_device.ip_address,
            site=new_device.site,
            fqdn=new_device.fqdn,
            vendor=new_device.vendor,
            model=new_device.model,
            operating_system=new_device.operating_system,
            os_version=new_device.os_version,
            username=new_device.username,
            hashed_password=hashed_password,
        )

        session.add(device)
        await session.commit()
        return device
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the device",
        )


@router.get("", response_model=list[DeviceResponse], status_code=200)
async def get_all_devices(
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Get a list of devices for currently logged in user"""
    try:
        devices = await session.execute(
            select(Device)
            .where(Device.user_id == current_user.id)
            .order_by(Device.name)
        )
        return devices.scalars().all()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the device",
        )


@router.get("/{device_id}", response_model=DeviceResponse, status_code=200)
async def get_device(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Device:

    result = await session.execute(select(Device).where(Device.id == device_id))
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    if device.user_id == current_user.id:
        return device
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Insufficient permissions to access device",
        )


@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Delete a device by ID"""

    result = await session.execute(select(Device).where(Device.id == device_id))
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    if device.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid permissions to remove the device",
        )
    await session.delete(device)
    await session.commit()
    return {"message": "Device removed successfully"}
