from datetime import datetime
from typing import Any, Union
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.deps.db import get_async_session
from app.models import User
from app.schemas import Token, TokenPayload
from sqlalchemy import func, select
from app.core.security import JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, ALGORITHM


from jose import jwt
from pydantic import ValidationError


oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", scheme_name="JWT")


async def current_user(
    session: AsyncSession = Depends(get_async_session), token: str = Depends(oauth2)
) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = await session.get(token_data.sub, None)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user"
        )

    return User(**user)


async def current_active_user(
    current_user: User = Depends(current_user),
) -> User:
    user = current_user
    if not user.is_active:
        raise HTTPException(
            status_code=400, detail="The user doesn't have valid permissions"
        )
    return user


async def current_superuser(
    current_user: User = Depends(current_user),
) -> User:
    user = current_user
    if not user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have valid permissions"
        )
    return user
