from typing import AsyncGenerator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.session import async_session
from app.models import User, UserSession

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
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                    )
                return user
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request"
            )
    except Exception as e:
        print(e)


# JWT-Based Implementation
# async def get_current_user(
#     session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
# ) -> User:

#     try:
#         payload = jwt.decode(
#             token, config.settings.SECRET_KEY, algorithms=[security.JWT_ALGORITHM]
#         )
#     except (jwt.DecodeError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials.",
#         )
#     # JWT guarantees payload will be unchanged (and thus valid), no errors here
#     token_data = security.JWTTokenPayload(**payload)

#     if token_data.refresh:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials, cannot use refresh token",
#         )
#     now = int(time.time())
#     if now < token_data.issued_at or now > token_data.expires_at:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials, token expired or not yet valid",
#         )

#     result = await session.execute(select(User).where(User.id == token_data.sub))
#     user: User | None = result.scalars().first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found.")
#     return user
