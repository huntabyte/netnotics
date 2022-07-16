from typing import Any, List
from fastapi import HTTPException, status

from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.security import hash_password

from app.deps.db import get_async_session
from app.deps.users import get_current_user
from app.models.user import User
from app.schemas.requests import UserCreateRequest
from app.schemas.responses import UserResponse

router = APIRouter()


@router.get(
    "/me", summary="Return logged in user information", response_model=UserResponse
)
async def read_curent_user(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Get the current logged in user"""
    return current_user


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Delete the current user
    """
    await session.execute(delete(User).where(User.email == current_user.email))
    await session.commit()


## TODO : Add reset password functionality


@router.post("/register", summary="Create new user", response_model=UserResponse)
async def register_user(
    user_in: UserCreateRequest,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    """
    Register a new user account
    """
    result = await session.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=hash_password(user_in.password),
    )
    session.add(user)
    await session.commit()
    return user


# @router.get("/users", response_model=List[UserSchema])
# async def get_users(
#     response: Response,
#     session: AsyncSession = Depends(get_async_session),
#     user: User = Depends(current_superuser),
#     skip: int = 0,
#     limit: int = 100,
# ) -> Any:
#     total = await session.scalar(select(func.count(User.id)))
#     users = (
#         (await session.execute(select(User).offset(skip).limit(limit))).scalars().all()
#     )
#     response.headers["Content-Range"] = f"{skip}-{skip + len(users)}/{total}"
#     return users
