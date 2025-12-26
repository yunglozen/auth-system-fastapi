from fastapi import APIRouter

from .v1 import auth
from .v1 import profile
from .v1 import services
from .v1 import admin

v1_router = APIRouter(tags=["v1_all"], prefix="/api/v1")


v1_router.include_router(auth.router)
v1_router.include_router(profile.router)
v1_router.include_router(services.router)
v1_router.include_router(admin.router)
