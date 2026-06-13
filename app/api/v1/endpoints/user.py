import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.api.validators import check_telegram_id_duplicate
from app.core.dependencies import RedisDep, SessionDep
from app.core.logger import setup_logger
from app.core.user import auth_backend, current_user, fastapi_users, get_jwt_strategy
from app.models.user import User
from app.schemas.user import (
    TelegramLinkByCodeRequest,
    TelegramLinkRequest,
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
