import httpx
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram_bot.keyboards import main_menu_keyboard
from telegram_bot.states import AuthStates
from telegram_bot.storage import API_URL, user_tokens

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для трекинга тренировок.",
        reply_markup=main_menu_keyboard,
    )


@router.message(F.text == "🔑 Войти")
async def cmd_login(message: Message, state: FSMContext):
    await message.answer("Введи email:")
    await state.set_state(AuthStates.waiting_email)


@router.message(AuthStates.waiting_email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введи пароль:")
    await state.set_state(AuthStates.waiting_password)


@router.message(AuthStates.waiting_password)
async def process_password(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    email = data["email"]
    password = message.text

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/auth/jwt/login",
            data={"username": email, "password": password},
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            user_tokens[message.from_user.id] = token

            await client.post(
                f"{API_URL}/users/link-telegram",
                headers={"Authorization": f"Bearer {token}"},
                json={"telegram_id": message.from_user.id},
            )

            await message.answer("✅ Успешно вошёл!")
        else:
            await message.answer("❌ Неверный email или пароль.")

    await state.clear()
