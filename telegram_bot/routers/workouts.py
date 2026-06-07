import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from telegram_bot.states import AddExerciseStates, CreateWorkoutStates
from telegram_bot.storage import API_URL, user_tokens

router = Router()


@router.message(F.text == "💪 Мои тренировки")
async def get_workouts(message: Message):
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

    for w in workouts:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📋 Подробнее", callback_data=f"workout_{w['id']}"
                    ),
                    InlineKeyboardButton(
                        text="🗑 Удалить", callback_data=f"delete_{w['id']}"
                    ),
                ]
            ]
        )
        await message.answer(f"💪 {w['name']}", reply_markup=kb)


@router.callback_query(F.data.startswith("workout_"))
async def get_workout_detail(callback: CallbackQuery):
    workout_id = callback.data.split("_")[1]
    token = user_tokens.get(callback.from_user.id)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/workouts/{workout_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    workout = response.json()
    text = f"*{workout['name']}*\n\n"
    for we in workout.get("workout_exercises", []):
        text += f"• {we['exercise']['name']} — {we['sets']}x{we['reps']}\n"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Добавить упражнение",
                    callback_data=f"add_exercise_{workout_id}",
                )
            ]
        ]
    )

    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_workout(callback: CallbackQuery):
    workout_id = callback.data.split("_")[1]
    token = user_tokens.get(callback.from_user.id)

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{API_URL}/workouts/{workout_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code == 204:
        await callback.message.answer("🗑 Тренировка удалена.")
    else:
        await callback.message.answer("❌ Что-то пошло не так.")

    await callback.answer()


@router.message(F.text == "➕ Создать тренировку")
async def cmd_create_workout(message: Message, state: FSMContext):
    token = user_tokens.get(message.from_user.id)
    if not token:
        await message.answer("Сначала войди — нажми 🔑 Войти")
        return
    await message.answer("Введи название тренировки:")
    await state.set_state(CreateWorkoutStates.waiting_name)


@router.message(CreateWorkoutStates.waiting_name)
async def process_workout_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введи описание (или напиши 'пропустить'):")
    await state.set_state(CreateWorkoutStates.waiting_description)


@router.message(CreateWorkoutStates.waiting_description)
async def process_workout_description(message: Message, state: FSMContext):
    data = await state.get_data()
    token = user_tokens.get(message.from_user.id)

    description = None if message.text.lower() == "пропустить" else message.text

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/workouts/",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": data["name"], "description": description},
        )

    if response.status_code == 200:
        await message.answer(f"✅ Тренировка '{data['name']}' создана!")
    else:
        await message.answer("❌ Что-то пошло не так.")

    await state.clear()


@router.callback_query(F.data.startswith("add_exercise_"))
async def cmd_add_exercise(callback: CallbackQuery, state: FSMContext):
    workout_id = callback.data.split("_")[2]
    await state.update_data(workout_id=workout_id)
    await callback.message.answer("Введи название упражнения:")
    await state.set_state(AddExerciseStates.waiting_exercise_name)
    await callback.answer()


@router.message(AddExerciseStates.waiting_exercise_name)
async def process_exercise_name(message: Message, state: FSMContext):
    await state.update_data(exercise_name=message.text)
    await message.answer("Введи количество подходов:")
    await state.set_state(AddExerciseStates.waiting_sets)


@router.message(AddExerciseStates.waiting_sets)
async def process_sets(message: Message, state: FSMContext):
    await state.update_data(sets=int(message.text))
    await message.answer("Введи количество повторений:")
    await state.set_state(AddExerciseStates.waiting_reps)


@router.message(AddExerciseStates.waiting_reps)
async def process_reps(message: Message, state: FSMContext):
    data = await state.get_data()
    token = user_tokens.get(message.from_user.id)

    async with httpx.AsyncClient() as client:
        exercise_response = await client.post(
            f"{API_URL}/exercises/",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": data["exercise_name"]},
        )
        exercise = exercise_response.json()

        await client.post(
            f"{API_URL}/workouts/{data['workout_id']}/exercises",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "exercise_id": exercise["id"],
                "sets": data["sets"],
                "reps": int(message.text),
            },
        )

    await message.answer("✅ Упражнение добавлено!")
    await state.clear()
