from time import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.config import settings
from app.deps.db import get_async_session
from app.models import User
from app.core.security import JWTTokenPayload
from sqlalchemy import select
from app.core.security import ALGORITHM


from jose import jwt
from pydantic import ValidationError


oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", scheme_name="JWT")


async def get_current_user(
    session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2)
) -> User:

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, alogirthms=[ALGORITHM])
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )

    token_data = JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.email == token_data.sub))
    user: User | None = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user
