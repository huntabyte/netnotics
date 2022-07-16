from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Device, User


async def test_create_new_device(
    client: AsyncClient, default_user_headers, default_user: User
):
    response = await client.post(
        app.url_path_for("create_device"),
        headers=default_user_headers,
        json={
            "name": "router",
            "ip_address": "127.0.0.1",
            "user_id": str(default_user.id),
        },
    )
    assert response.status_code == 201
    result = response.json()
    assert result["user_id"] == str(default_user.id)
    assert result["name"] == "router"
    assert result["ip_address"] == "127.0.0.1"


async def test_get_all_devices(
    client: AsyncClient, default_user_headers, default_user: User, session: AsyncSession
):
    device1 = Device(name="device1", ip_address="127.0.0.1", user_id=default_user.id)
    device2 = Device(name="device2", ip_address="127.0.0.2", user_id=default_user.id)
    session.add(device1)
    session.add(device2)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_all_devices"), headers=default_user_headers
    )
    assert response.status_code == 200

    assert response.json() == [
        {
            "user_id": str(device1.user_id),
            "name": device1.name,
            "ip_address": device1.ip_address,
            "id": device1.id,
        },
        {
            "user_id": str(device2.user_id),
            "name": device2.name,
            "ip_address": device2.ip_address,
            "id": device2.id,
        },
    ]
