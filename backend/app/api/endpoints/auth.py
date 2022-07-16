import time
import uuid

import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import config, security
from app.models import User, UserSession
from app.schemas.requests import RefreshTokenRequest
from app.schemas.responses import AccessTokenResponse, SessionResponse

router = APIRouter()


@router.post("/access-token", response_model=AccessTokenResponse)
async def login_access_token(
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """OAuth2 compatible token, get an access token for future requests using username and password"""

    result = await session.execute(select(User).where(User.email == form_data.username))
    user: User | None = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return security.generate_access_token_response(str(user.id))


@router.post("/refresh-token", response_model=AccessTokenResponse)
async def refresh_token(
    input: RefreshTokenRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """OAuth2 compatible token, get an access token for future requests using refresh token"""
    try:
        payload = jwt.decode(
            input.refresh_token,
            config.settings.SECRET_KEY,
            algorithms=[security.JWT_ALGORITHM],
        )
    except (jwt.DecodeError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, unknown error",
        )

    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    if not token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use access token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user: User | None = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return security.generate_access_token_response(str(user.id))


@router.post("/login")
async def login_user(
    response: Response,
    session: AsyncSession = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Login user and return session cookie"""
    result = await session.execute(select(User).where(User.email == form_data.username))
    user: User | None = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    await session.execute(delete(UserSession).where(UserSession.user_id == user.id))
    await session.commit()
    user_session = UserSession(user_id=user.id, expires_at=int(time.time()) + 1152)
    session.add(user_session)
    await session.commit()

    response.set_cookie(
        key="session_id",
        value=user_session.id,
        expires=int(time.time() + 11520),
        path="/",
        httponly=True,
    )

    return {"message": "Success"}


@router.post("/logout")
async def logout_user(
    response: Response,
    request: Request,
    session: AsyncSession = Depends(deps.get_session),
):
    """Login user and return session cookie"""
    try:
        cookie_id = request.cookies.get("session_id")
        print(cookie_id)
        result = await session.execute(
            select(UserSession).where(UserSession.id == cookie_id)
        )
        user_session: UserSession | None = result.scalars().first()
        await session.delete(user_session)
        await session.commit()

        raise Exception("error")
    except Exception as error:
        print(error)

    response.set_cookie(
        key="session_id",
        value="",
        expires="",
        path="/",
        httponly=True,
    )

    return {"message": "Success"}


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: uuid.UUID, session: AsyncSession = Depends(deps.get_session)
):
    """Get status of a session"""
    try:
        result = await session.execute(
            select(UserSession).where(UserSession.id == session_id)
        )
        user_session: UserSession | None = result.scalars().first()
        raise Exception
    except Exception as error:
        print(error)

    if user_session is None:
        return {"authenticated": False}

    return {"authenticated": True, "user_id": user_session.user_id}
