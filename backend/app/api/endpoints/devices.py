from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.api.deps import CommonDeps
from app.services.restconf import RESTCONF
from app.models import Device, User
from app.schemas.requests import DeviceCreateRequest
from app.schemas.responses import DeviceDataResponse, DeviceResponse

router = APIRouter()


@router.post("", response_model=DeviceResponse, status_code=201)
async def create_device(
    new_device: DeviceCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
) -> DeviceResponse:
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
        await device.is_manageable
        session.add(device)
        await session.commit()
        return device
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the device",
        )


@router.get("", response_model=list[DeviceResponse], status_code=200)
async def get_all_devices(
    devices: list[Device] = Depends(deps.get_many_devices),
) -> list[DeviceResponse]:
    """Get a list of devices for currently logged in user"""
    return devices


@router.get("/{device_id}", response_model=DeviceResponse, status_code=200)
async def get_device(device: Device = Depends(deps.get_device)) -> DeviceResponse:
    await device.is_manageable

    return device


@router.delete("/{device_id}", status_code=200)
async def delete_device(
    device: Device = Depends(deps.get_device), commons: CommonDeps = Depends(CommonDeps)
) -> Any:
    """Delete a device by ID"""
    await commons.session.delete(device)
    await commons.session.commit()
    return {"message": "Device removed successfully"}


@router.get("/{device_id}/restconf", response_model=DeviceDataResponse)
async def get_restconf_data(
    xpath: str = None,
    device: Device = Depends(deps.get_device),
) -> DeviceDataResponse:
    """
    Returns result of device query via RESTCONF with a custom xpath query param
    """
    if xpath is None:
        raise HTTPException(
            status_code=400,
            detail="A valid xpath parameter must be specified",
        )

    if not device.manageable:
        raise HTTPException(status_code=504, detail="Could not reach device")

    device_client = RESTCONF(
        host=device.fqdn, username=device.username, password=device.password
    )
    data = await device_client.get_xpath_data(xpath=f"/{xpath}")

    return {
        "device": device,
        "data": data,
    }


@router.get(
    "/{device_id}/interfaces",
    response_model=DeviceDataResponse,
)
async def get_device_interfaces(
    name: Optional[str] = None,
    device: Device = Depends(deps.get_managed_device),
    commons: CommonDeps = Depends(CommonDeps),
) -> DeviceDataResponse:
    """
    Returns a list of interfaces belonging to the device
    """

    device_client = RESTCONF(
        host=device.fqdn, username=device.username, password=device.password
    )

    if name:
        interface = await device_client.get_interface_details(name)
        return {"device": device, "data": interface}

    interfaces = await device_client.get_interface_details()

    return {"device": device, "data": interfaces}


@router.get(
    "/{device_id}/restconf/verify", dependencies=[Depends(deps.get_managed_device)]
)
async def verify_restconf_connection():
    """
    Verifies the restconf connection to the device specified by device_id
    """
    return {"success": True}
