from app.core.config import settings

user_tokens: dict = {}
API_URL = settings.api_url
TOKEN_TTL = 86400 * 30


async def get_token(telegram_id: int) -> str | None:
    return user_tokens.get(telegram_id)


async def set_token(telegram_id: int, token: str) -> None:
    user_tokens[telegram_id] = token
