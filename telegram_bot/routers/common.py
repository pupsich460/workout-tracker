from http import HTTPStatus

import httpx
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.storage import API_URL, set_token

router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Нечего отменять.")
        return

    await state.clear()
    await message.answer("❌ Текущее действие отменено.")


@router.message(F.text == "🔑 Авторизоваться")
async def cmd_reauth(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/telegram/auth",
            json={"telegram_id": message.from_user.id},
        )

    if response.status_code == HTTPStatus.OK:
        token = response.json().get("access_token")
        if token:
            await set_token(message.from_user.id, token)
            await message.answer("✅ Авторизация прошла успешно!")
        else:
            await message.answer("❌ Не удалось получить токен.")
    else:
        await message.answer("❌ Аккаунт не найден. Привяжи Telegram через /link CODE")
