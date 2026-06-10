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


# @router.post("/link-telegram")
# async def link_telegram(
#     data: TelegramLinkRequest,
#     session: SessionDep,
#     user: User = Depends(current_user),
# ):
#     """Привязать Telegram к аккаунту."""
#     await check_telegram_id_duplicate(data.telegram_id, session)
#     user.telegram_id = data.telegram_id
#     session.add(user)
#     await session.commit()
#     logger.info(f"Пользователь {user.email} привязал Telegram ID {data.telegram_id}")

#     return {
#         "detail": "Telegram привязан",
#         "email": user.email,
#     }


# @router.post("/telegram-link-code")
# async def generate_telegram_link_code(
#     session: SessionDep,
#     user: User = Depends(current_user),
# ):
#     """Сгенерировать код для привязки Telegram."""
#     code = secrets.token_urlsafe(8)

#     user.telegram_link_code = code
#     session.add(user)
#     await session.commit()

#     logger.info(f"Пользователь {user.email} сгенерировал код для привязки Telegram")

#     return {"telegram_link_code": code}


# @router.post("/link-telegram-by-code")
# async def link_telegram_by_code(
#     data: TelegramLinkByCodeRequest,
#     session: SessionDep,
# ):
#     user = await session.scalar(
#         select(User).where(User.telegram_link_code == data.code)
#     )

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Invalid link code",
#         )

#     await check_telegram_id_duplicate(data.telegram_id, session)

#     user.telegram_id = data.telegram_id
#     user.telegram_link_code = None

#     session.add(user)
#     await session.commit()

#     strategy = get_jwt_strategy()
#     access_token = await strategy.write_token(user)

#     logger.info(f"Пользователь {user.email} привязал Telegram ID {data.telegram_id}")

#     return {
#         "detail": "Telegram привязан",
#         "email": user.email,
#         "access_token": access_token,
#     }
