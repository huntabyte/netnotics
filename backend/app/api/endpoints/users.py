import time
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.deps import CommonDeps
from app.core.security import get_password_hash
from app.models import UserSession, User
from app.schemas.requests import UserCreateRequest, UserUpdatePasswordRequest
from app.schemas.responses import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(commons: CommonDeps = Depends(CommonDeps)):
    """Get current user"""
    return commons.current_user


@router.delete("/me", status_code=204)
async def delete_current_user(commons: CommonDeps = Depends(CommonDeps)):
    """Delete current user"""
    await commons.session.execute(
        delete(User).where(User.id == commons.current_user.id)
    )
    await commons.session.commit()


@router.post("/reset-password", response_model=UserResponse)
async def reset_current_user_password(
    user_update_password: UserUpdatePasswordRequest,
    commons: CommonDeps = Depends(CommonDeps),
):
    """Update current user password"""
    commons.current_user.hashed_password = get_password_hash(
        user_update_password.password
    )
    commons.session.add(commons.current_user)
    await commons.session.commit()
    return commons.current_user


@router.post("/register", response_model=UserResponse)
async def register_new_user(
    response: Response,
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new user"""
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password),
        name=new_user.name,
    )
    session.add(user)
    await session.commit()
    user_session = UserSession(user_id=user.id, expires_at=int(time.time()) + 11520)
    session.add(user_session)
    await session.commit()

    response.set_cookie(
        key="session_id",
        value=user_session.id,
        expires=int(time.time()) + 11520,
        path="/",
        httponly=True,
    )

    return user
