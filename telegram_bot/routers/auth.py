import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from telegram_bot.keyboards import main_menu_keyboard
from telegram_bot.storage import API_URL, user_tokens

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для трекинга тренировок.\n\n"
        "Чтобы привязать аккаунт:\n"
        "1. Войди в API.\n"
        "2. Получи код привязки Telegram.\n"
        "3. Отправь сюда команду:\n\n"
        "/link CODE",
        reply_markup=main_menu_keyboard,
    )


@router.message(Command("link"))
async def cmd_link(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Отправь команду в формате:\n\n/link CODE")
        return

    code = args[1].strip()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/link-telegram-by-code",
            json={
                "telegram_id": message.from_user.id,
                "code": code,
            },
        )

    if response.status_code == 200:
        data = response.json()
        email = data.get("email")

        token = data.get("access_token")
        if token:
            user_tokens[message.from_user.id] = token

        if email:
            await message.answer(f"✅ Telegram привязан к аккаунту {email}")
        else:
            await message.answer("✅ Telegram успешно привязан к аккаунту")
    elif response.status_code == 404:
        await message.answer("❌ Неверный код привязки")
    elif response.status_code == 400:
        await message.answer("❌ Этот Telegram уже привязан к другому аккаунту")
    else:
        await message.answer("❌ Не удалось привязать Telegram. Попробуй позже.")
