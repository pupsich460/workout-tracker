from app.core.config import settings
from app.core.redis import redis_client

API_URL = settings.api_url
TOKEN_TTL = 86400 * 30


async def get_token(telegram_id: int) -> str | None:
    return await redis_client.get(f"tg_token:{telegram_id}")


async def set_token(telegram_id: int, token: str) -> None:
    await redis_client.set(f"tg_token:{telegram_id}", token, ex=TOKEN_TTL)
