from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import auth_backend, current_user, fastapi_users
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

router = APIRouter()

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


@router.post("/link-telegram")
async def link_telegram(
    telegram_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Привязать Telegram к аккаунту."""
    user.telegram_id = telegram_id
    session.add(user)
    await session.commit()
    return {"detail": "Telegram привязан"}
