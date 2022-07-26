from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.api.deps import CommonDeps
from app.services.restconf import RESTCONF, DeviceConnection
from app.models import Device
from app.schemas.requests import DeviceCreateRequest, DeviceUpdateRequest
from app.schemas.responses import DeviceDataResponse, DeviceResponse

router = APIRouter()


@router.post("", response_model=DeviceResponse, status_code=201)
async def create_device(
    new_device: DeviceCreateRequest, commons: CommonDeps = Depends(CommonDeps)
) -> DeviceResponse:
    """
    Creates a new device. Only for logged in users.
    """

    try:
        device = Device(
            user_id=commons.current_user.id,
            name=new_device.name,
            ip_address=new_device.ip_address,
            host=new_device.host,
            username=new_device.username,
            password=new_device.password,
            manageable=new_device.manageable,
        )
        await device.is_manageable
        commons.session.add(device)
        await commons.session.commit()
        return device
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the device",
        )


@router.put("/{device_id}", response_model=DeviceResponse, status_code=200)
async def update_device(
    updated_device: DeviceUpdateRequest,
    commons: CommonDeps = Depends(CommonDeps),
    device: Device = Depends(deps.get_device),
):
    """Update a device by ID"""
    if updated_device.name:
        device.name = updated_device.name
    if updated_device.ip_address:
        device.ip_address = updated_device.ip_address
    if updated_device.host:
        device.host = updated_device.host
    if updated_device.username:
        device.username = updated_device.username
    if updated_device.password:
        device.password = updated_device.password
    await commons.session.commit()
    return device


@router.get("", response_model=list[DeviceResponse], status_code=200)
async def get_all_devices(
    devices: list[Device] = Depends(deps.get_many_devices),
) -> list[DeviceResponse]:
    """Get a list of devices for currently logged in user"""
    return devices


@router.get("/{device_id}", response_model=DeviceResponse, status_code=200)
async def get_device(device: Device = Depends(deps.get_device)) -> DeviceResponse:
    """Get a single device by ID"""
    return device


@router.get("/{device_id}/detect")
def get_device_type(device: Device = Depends(deps.get_device)) -> Any:
    """Detect the device type"""
    connection = DeviceConnection(
        host=device.host, username=device.username, password=device.password
    )
    type = connection.auto_detect()
    print(type)
    return {"type": type}


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
        host=device.host, username=device.username, password=device.password
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
    device: Device = Depends(deps.get_device),
) -> DeviceDataResponse:
    """
    Returns a list of interfaces belonging to the device
    """

    device_client = RESTCONF(
        host=device.host, username=device.username, password=device.password
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
