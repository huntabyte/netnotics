from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Device, User
from app.schemas.requests import DeviceCreateRequest
from app.schemas.responses import DeviceResponse

router = APIRouter()


@router.post("/", response_model=DeviceResponse, status_code=201)
async def create_device(
    new_device: DeviceCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Creates a new device. Only for logged in users.
    """

    device = Device(
        user_id=current_user.id, name=new_device.name, ip_address=new_device.ip_address
    )

    session.add(device)
    await session.commit()
    return device


@router.get("/", response_model=list[DeviceResponse], status_code=200)
async def get_all_devices(
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Get a list of devices for currently logged in user"""

    devices = await session.execute(
        select(Device).where(Device.user_id == current_user.id).order_by(Device.name)
    )
    return devices.scalars().all()
