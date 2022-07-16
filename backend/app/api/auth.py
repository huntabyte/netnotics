import time
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from jose import jwt
from app.core.config import settings

from app.deps.db import get_async_session
from app.models.user import User
from app.schemas.requests import RefreshTokenRequest
from app.schemas.responses import AccessTokenResponse
from app.core.security import (
    ALGORITHM,
    generate_access_token_response,
    verify_password,
)

router = APIRouter(prefix="/auth")


@router.post(
    "/token",
    summary="Create access and refresh tokens",
    response_model=AccessTokenResponse,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    OAuth2 compatible token, get an access token for future requests using username and password
    """
    result = await session.execute(select(User).where(User.email == form_data.username))
    user: User | None = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST, detail="User not found"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect login credentials",
        )
    return generate_access_token_response(str(user.email))


@router.post(
    "/refresh", summary="Refresh access token", response_model=AccessTokenResponse
)
async def refresh_token(
    input: RefreshTokenRequest, session: AsyncSession = Depends(get_async_session)
) -> Any:
    """
    OAuth2 Compatible token, get an access token for future requests using refresh token
    """
    try:
        payload = jwt.decode(
            input.refresh_token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    token_data = AccessTokenResponse(**payload)

    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use access token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validation credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.email == token_data.sub))
    user: User | None = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return generate_access_token_response(str(user.email))
