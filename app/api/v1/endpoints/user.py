
from fastapi import APIRouter

from app.core.logger import setup_logger
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)

router = APIRouter()

logger = setup_logger(__name__)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
