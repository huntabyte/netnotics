from fastapi import APIRouter

from app.api import devices, users, utils, auth

api_router = APIRouter()

api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(devices.router, tags=["devices"])
api_router.include_router(auth.router, tags=["auth"])
