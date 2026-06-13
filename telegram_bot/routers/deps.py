from aiogram.types import CallbackQuery, Message

from telegram_bot.services.auth import get_or_restore_token


async def require_token(message_or_callback) -> str | None:
    token = await get_or_restore_token(message_or_callback.from_user.id)

    if not token:
        target = (
            message_or_callback.message
            if isinstance(message_or_callback, CallbackQuery)
            else message_or_callback
        )
        await target.answer("Сначала привяжи аккаунт через /link CODE")

    return token
