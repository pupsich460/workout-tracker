from http import HTTPStatus

import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from telegram_bot.keyboards import goal_keyboard, level_keyboard
from telegram_bot.services.auth import get_or_restore_token
from telegram_bot.states import GenerateStates
from telegram_bot.storage import API_URL

router = Router()


@router.message(F.text == "🤖 Сгенерировать тренировку")
async def cmd_generate(message: Message, state: FSMContext):
    token = await get_or_restore_token(message.from_user.id)

    if not token:
        await message.answer("Сначала привяжи аккаунт через /link CODE")
        return

    await message.answer(
        "Выбери цель тренировки:",
        reply_markup=goal_keyboard,
    )
    await state.set_state(GenerateStates.waiting_goal)


@router.callback_query(GenerateStates.waiting_goal)
async def process_goal(callback: CallbackQuery, state: FSMContext):
    goal = callback.data.replace("goal_", "")

    await state.update_data(goal=goal)

    await callback.message.answer("Введи текущий вес (кг):")
    await callback.answer()

    await state.set_state(GenerateStates.waiting_weight)


@router.message(GenerateStates.waiting_weight)
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(current_weight=weight)

    await message.answer("Сколько тренировок в неделю?")
    await state.set_state(GenerateStates.waiting_days)


@router.message(GenerateStates.waiting_days)
async def process_days(message: Message, state: FSMContext):
    try:
        days = int(message.text)
    except ValueError:
        await message.answer("Введите число.")
        return

    await state.update_data(days_per_week=days)

    await message.answer(
        "Выбери уровень подготовки:",
        reply_markup=level_keyboard,
    )
    await state.set_state(GenerateStates.waiting_level)


@router.callback_query(GenerateStates.waiting_level)
async def process_level(callback: CallbackQuery, state: FSMContext):
    token = await get_or_restore_token(callback.from_user.id)

    if not token:
        await callback.message.answer("Сначала привяжи аккаунт через /link CODE")
        await callback.answer()
        await state.clear()
        return

    data = await state.get_data()

    level = callback.data.replace("level_", "")

    await callback.message.answer("⏳ Генерирую тренировку...")
    await callback.answer()

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{API_URL}/workouts/ai/generate",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "goal": data["goal"],
                "current_weight": data["current_weight"],
                "days_per_week": data["days_per_week"],
                "level": level,
            },
        )

    if response.status_code != HTTPStatus.OK:
        await callback.message.answer("❌ Не удалось сгенерировать тренировку.")
        await state.clear()
        return

    workout = response.json()

    text = f"✅ Тренировка создана: *{workout['name']}*\n\n"

    for we in workout.get("workout_exercises", []):
        text += f"• {we['exercise']['name']} — {we['sets']}x{we['reps']}\n"

    await callback.message.answer(
        text,
        parse_mode="Markdown",
    )

    await state.clear()
