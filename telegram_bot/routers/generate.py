import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from telegram_bot.keyboards import level_keyboard
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

    await message.answer("Введи цель (например: похудеть, набрать массу):")
    await state.set_state(GenerateStates.waiting_goal)


@router.message(GenerateStates.waiting_goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer("Введи текущий вес (кг):")
    await state.set_state(GenerateStates.waiting_weight)


@router.message(GenerateStates.waiting_weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(current_weight=int(message.text))
    await message.answer("Сколько тренировок в неделю?")
    await state.set_state(GenerateStates.waiting_days)


@router.message(GenerateStates.waiting_days)
async def process_days(message: Message, state: FSMContext):
    await state.update_data(days_per_week=int(message.text))
    await message.answer("Уровень подготовки:", reply_markup=level_keyboard)
    await state.set_state(GenerateStates.waiting_level)


@router.callback_query(GenerateStates.waiting_level)
async def process_level(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    token = await get_or_restore_token(callback.from_user.id)

    if not token:
        await callback.message.answer("Сначала привяжи аккаунт через /link CODE")
        await callback.answer()
        await state.clear()
        return

    level = callback.data

    await callback.message.answer("⏳ Генерирую тренировку...")
    await callback.answer()

    async with httpx.AsyncClient(timeout=30) as client:
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

    if response.status_code != 200:
        await callback.message.answer("❌ Не удалось сгенерировать тренировку.")
        await state.clear()
        return

    workout = response.json()
    text = f"✅ Тренировка создана: *{workout['name']}*\n\n"

    for we in workout.get("workout_exercises", []):
        text += f"• {we['exercise']['name']} — {we['sets']}x{we['reps']}\n"

    await callback.message.answer(text, parse_mode="Markdown")
    await state.clear()
