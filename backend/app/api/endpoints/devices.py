from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.services.restconf import RESTCONF
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
            password=new_device.password,
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

    result = await session.execute(
        select(Device).where(
            and_(Device.id == device_id, Device.user_id == current_user.id)
        )
    )
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    return device


@router.delete("/{device_id}", status_code=status.HTTP_200_OK)
async def delete_device(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """Delete a device by ID"""

    result = await session.execute(
        select(Device).where(
            and_(Device.id == device_id, Device.user_id == current_user.id)
        )
    )
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    await session.delete(device)
    await session.commit()
    return {"message": "Device removed successfully"}


@router.get("/{device_id}/os-version")
async def get_os_version(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Return the device's OS version"""

    result = await session.execute(
        select(Device).where(
            and_(Device.id == device_id, Device.user_id == current_user.id)
        )
    )
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    device_client = RESTCONF(
        host=device.fqdn, username=device.username, password=device.password
    )
    version = await device_client.get_os_version()
    if version:
        return {"version": version}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch the OS version for the given device.",
        )


@router.get("/{device_id}/restconf")
async def get_restconf_data(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    xpath: str = None,
):
    """
    Returns result of device query via RESTCONF with a custom xpath query param
    """
    if xpath is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid xpath parameter must be specified",
        )

    result = await session.execute(
        select(Device).where(
            and_(Device.id == device_id, Device.user_id == current_user.id)
        )
    )
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    device_client = RESTCONF(
        host=device.fqdn, username=device.username, password=device.password
    )
    return await device_client.get_xpath_data(xpath=f"/{xpath}")


@router.get("/{device_id}/interfaces")
async def get_device_interfaces(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Returns a list of interfaces belonging to the device
    """
    result = await session.execute(
        select(Device).where(
            and_(Device.id == device_id, Device.user_id == current_user.id)
        )
    )
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    device_client = RESTCONF(
        host=device.fqdn, username=device.username, password=device.password
    )
    return await device_client.get_interface_details()


@router.get("/{device_id}/restconf/verify")
async def verify_restconf_connection(
    device_id: int,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Verifies the restconf connection to the device specified by device_id
    """
    result = await session.execute(
        select(Device).where(
            and_(Device.id == device_id, Device.user_id == current_user.id)
        )
    )
    device: Device | None = result.scalars().first()

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )
    device_client = RESTCONF(
        host=device.fqdn, username=device.username, password=device.password
    )

    connected = await device_client.verify_connectivity()
    if not connected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to the device",
        )
    return {"message": "Successfully connected to the device"}
