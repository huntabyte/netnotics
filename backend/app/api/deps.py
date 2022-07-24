from typing import AsyncGenerator

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import async_session
from app.models import Device, User, UserSession

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> User:
    try:
        session_id = request.cookies.get("session_id")
        if session_id:
            result = await session.execute(
                select(UserSession).where(UserSession.id == session_id)
            )
            user_session: UserSession | None = result.scalars().first()

            if user_session:
                result = await session.execute(
                    select(User).where(User.id == user_session.user_id)
                )
                user: User | None = result.scalars().first()

                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                return user
        else:
            raise HTTPException(status_code=400, detail="Bad request")
    except Exception as e:
        print(e)


class CommonDeps:
    def __init__(
        self,
        q: str | None = None,
        skip: int = 0,
        limit: int = 0,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
    ):
        self.q = q
        self.skip = skip
        self.limit = limit
        self.current_user = current_user
        self.session = session


async def get_many_devices(commons: CommonDeps = Depends(CommonDeps)):
    try:
        result = await commons.session.execute(
            select(Device)
            .where(Device.user_id == commons.current_user.id)
            .order_by(Device.name)
        )
        devices = result.scalars().all()

        # await asyncio.gather(*[d.is_manageable for d in devices])

        return devices

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the device",
        )


async def get_device(device_id: int, commons: CommonDeps = Depends(CommonDeps)):
    try:
        result = await commons.session.execute(
            select(Device).where(
                and_(Device.id == device_id, Device.user_id == commons.current_user.id)
            )
        )
        device: Device | None = result.scalars().first()

        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")
        return device
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while retrieving the requested device.",
        )


async def get_managed_device(device: Device = Depends(get_device)):
    if not device.manageable:
        raise HTTPException(status_code=405, detail="Device is not manageable.")
    return device
