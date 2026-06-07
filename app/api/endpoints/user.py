from fastapi import APIRouter, Depends

from app.api.validators import check_telegram_id_duplicate
from app.core.dependencies import RedisDep, SessionDep
from app.core.logger import setup_logger
from app.core.user import auth_backend, current_user, fastapi_users
from app.models.user import User
from app.schemas.user import (TelegramLinkRequest, UserCreate, UserRead,
                              UserUpdate)

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


@router.post("/link-telegram")
async def link_telegram(
    data: TelegramLinkRequest,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Привязать Telegram к аккаунту."""
    await check_telegram_id_duplicate(data.telegram_id, session)
    user.telegram_id = data.telegram_id
    session.add(user)
    await session.commit()
    logger.info(f"Пользователь {user.username} привязал Telegram ID {data.telegram_id}")
    return {"detail": "Telegram привязан"}
