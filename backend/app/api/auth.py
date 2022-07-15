from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import Response

from app.deps.db import get_async_session
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate
from app.schemas import Token
from app.core.security import (
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)

router = APIRouter(prefix="/auth")


@router.post("/register", summary="Create new user", response_model=UserSchema)
async def register_user(
    *,
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Register a new user account
    """
    result = await session.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )
    user = user_in.dict()
    user["hashed_password"] = hash_password(user["password"])
    del user["password"]
    user = User(**user)
    session.add(user)
    await session.commit()
    return user


@router.post("/login", summary="Create access and refresh tokens", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
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
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
