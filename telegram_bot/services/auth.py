import httpx

from telegram_bot.storage import API_URL, get_token, set_token


async def get_or_restore_token(telegram_id: int) -> str | None:
    token = await get_token(telegram_id)

    if token:
        return token

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/telegram/auth",
            json={"telegram_id": telegram_id},
        )

    if response.status_code != 200:
        return None

    data = response.json()

    token = data["access_token"]

    await set_token(telegram_id, token)

    return token
