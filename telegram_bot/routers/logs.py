from http import HTTPStatus

import httpx
from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from telegram_bot.services.auth import get_or_restore_token
from telegram_bot.storage import API_URL

router = Router()


async def require_token(message_or_callback) -> str | None:
    user_id = message_or_callback.from_user.id
    token = await get_or_restore_token(user_id)

    if not token:
        target = (
            message_or_callback.message
            if isinstance(message_or_callback, CallbackQuery)
            else message_or_callback
        )
        await target.answer("Сначала привяжи аккаунт через /link CODE")

    return token


@router.message(F.text == "📝 Отметить тренировку")
async def cmd_log(message: Message):
    token = await require_token(message)
    if not token:
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/workouts/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code != HTTPStatus.OK:
        await message.answer("❌ Не удалось получить тренировки.")
        return

    workouts = response.json()
    if not workouts:
        await message.answer("У тебя пока нет тренировок.")
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=w["name"], callback_data=f"log_{w['id']}")]
            for w in workouts
        ]
    )
    await message.answer("Выбери тренировку, которую выполнил:", reply_markup=kb)


@router.callback_query(F.data.startswith("log_"))
async def process_log(callback: CallbackQuery):
    token = await require_token(callback)
    if not token:
        await callback.answer()
        return

    workout_id = int(callback.data.split("_")[1])

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/workout-logs/",
            headers={"Authorization": f"Bearer {token}"},
            json={"workout_id": workout_id, "status": True},
        )

    if response.status_code == HTTPStatus.CREATED:
        await callback.message.answer("✅ Тренировка отмечена как выполненная!")
    else:
        await callback.message.answer("❌ Что-то пошло не так.")

    await callback.answer()
