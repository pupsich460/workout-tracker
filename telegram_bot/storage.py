from sqlalchemy import select

from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.models.user import User

API_URL = settings.api_url

_user_tokens: dict[int, str] = {}


async def get_token(telegram_id: int) -> str | None:
    if telegram_id in _user_tokens:
        return _user_tokens[telegram_id]

    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if user and user.bot_token:
            _user_tokens[telegram_id] = user.bot_token
            return user.bot_token

    return None


async def set_token(telegram_id: int, token: str) -> None:
    _user_tokens[telegram_id] = token

    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if user:
            user.bot_token = token
            session.add(user)
            await session.commit()
