import httpx
from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from telegram_bot.storage import API_URL, user_tokens

router = Router()


@router.message(F.text == "📝 Отметить тренировку")
async def cmd_log(message: Message):
    token = user_tokens.get(message.from_user.id)
    if not token:
        await message.answer("Сначала войди — нажми 🔑 Войти")
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/workouts/",
            headers={"Authorization": f"Bearer {token}"},
        )

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
    await message.answer("Выбери тренировку которую выполнил:", reply_markup=kb)


@router.callback_query(F.data.startswith("log_"))
async def process_log(callback: CallbackQuery):
    workout_id = int(callback.data.split("_")[1])
    token = user_tokens.get(callback.from_user.id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/workout-logs/",
            headers={"Authorization": f"Bearer {token}"},
            json={"workout_id": workout_id},
        )

    if response.status_code == 201:
        await callback.message.answer("✅ Тренировка отмечена как выполненная!")
    else:
        await callback.message.answer("❌ Что-то пошло не так.")

    await callback.answer()
