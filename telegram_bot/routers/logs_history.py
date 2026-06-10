import httpx
from aiogram import F, Router
from aiogram.types import Message

from telegram_bot.services.auth import get_or_restore_token
from telegram_bot.storage import API_URL

router = Router()


@router.message(F.text == "📊 История тренировок")
async def get_workout_logs(message: Message):
    token = await get_or_restore_token(message.from_user.id)

    if not token:
        await message.answer("Сначала привяжи аккаунт через /link CODE")
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/workout-logs/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code != 200:
        await message.answer("❌ Не удалось получить историю тренировок.")
        return

    logs = response.json()

    if not logs:
        await message.answer("История тренировок пока пустая.")
        return

    text = "📊 *История тренировок:*\n\n"

    for log in logs[-10:]:
        status = "✅ Выполнена" if log.get("status") else "❌ Не выполнена"
        date = log.get("date", "Дата не указана")
        workout_id = log.get("workout_id", "—")

        text += f"{status}\n" f"🏋️ Тренировка ID: {workout_id}\n" f"📅 Дата: {date}\n\n"

    await message.answer(text, parse_mode="Markdown")
