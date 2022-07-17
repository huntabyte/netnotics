from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import User
from app.tests.conftest import default_user_email, default_user_id, default_user_name


async def test_read_current_user(client: AsyncClient, default_user_cookie):
    response = await client.get(
        app.url_path_for("read_current_user"), cookies=default_user_cookie
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(default_user_id),
        "email": default_user_email,
        "name": default_user_name,
    }


async def test_delete_current_user(
    client: AsyncClient, default_user_cookie, session: AsyncSession
):
    response = await client.delete(
        app.url_path_for("delete_current_user"), cookies=default_user_cookie
    )
    assert response.status_code == 204
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is None


# async def test_reset_current_user_password(
#     client: AsyncClient, , session: AsyncSession
# ):
#     response = await client.post(
#         app.url_path_for("reset_current_user_password"),
#     ,
#         json={"password": "testxxxxxx"},
#     )
#     assert response.status_code == 200
#     result = await session.execute(select(User).where(User.id == default_user_id))
#     user: User | None = result.scalars().first()
#     assert user is not None
#     assert user.hashed_password != default_user_password_hash


async def test_register_new_user(client: AsyncClient, session: AsyncSession):
    response = await client.post(
        app.url_path_for("register_new_user"),
        headers={"Content-Type": "application/json"},
        json={
            "email": "qwe@example.com",
            "password": "asdasdasd",
        },
    )
    assert response.status_code == 200
    result = await session.execute(select(User).where(User.email == "qwe@example.com"))
    user: User | None = result.scalars().first()
    assert user is not None
