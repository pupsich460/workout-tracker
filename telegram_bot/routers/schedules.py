import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from telegram_bot.keyboards import reminder_minutes_keyboard
from telegram_bot.services.auth import get_or_restore_token
from telegram_bot.states import ScheduleStates
from telegram_bot.storage import API_URL

router = Router()

WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}


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


@router.message(F.text == "⏰ Напоминания")
async def show_schedules_menu(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Мои напоминания",
                    callback_data="schedules_list",
                )
            ],
            [
                InlineKeyboardButton(
                    text="➕ Создать напоминание",
                    callback_data="schedules_create",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Удалить напоминание",
                    callback_data="schedules_delete",
                )
            ],
        ]
    )

    await message.answer("Выбери действие:", reply_markup=kb)


@router.callback_query(F.data == "schedules_list")
async def list_schedules(callback: CallbackQuery):
    token = await require_token(callback)
    if not token:
        await callback.answer()
        return

    async with httpx.AsyncClient() as client:
        schedules_response = await client.get(
            f"{API_URL}/workout-schedules/schedules/",
            headers={"Authorization": f"Bearer {token}"},
        )

        workouts_response = await client.get(
            f"{API_URL}/workouts/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if schedules_response.status_code != 200:
        await callback.message.answer("❌ Не удалось получить напоминания.")
        await callback.answer()
        return

    schedules = schedules_response.json()

    if not schedules:
        await callback.message.answer("У тебя пока нет напоминаний.")
        await callback.answer()
        return

    workouts_by_id = {}

    if workouts_response.status_code == 200:
        workouts_by_id = {
            workout["id"]: workout["name"] for workout in workouts_response.json()
        }

    text = "⏰ *Твои напоминания:*\n\n"

    for schedule in schedules:
        weekday = WEEKDAYS.get(schedule["weekday"], "Неизвестно")
        status = "🟢 Активно" if schedule["is_active"] else "🔴 Неактивно"

        workout_name = workouts_by_id.get(
            schedule["workout_id"],
            f"ID {schedule['workout_id']}",
        )

        text += (
            f"🏋️ *{workout_name}*\n"
            f"📅 {weekday}\n"
            f"🕒 {schedule['workout_time']}\n"
            f"⏳ Напомнить за {schedule['reminder_minutes_before']} мин.\n"
            f"{status}\n\n"
        )

    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "schedules_create")
async def start_create_schedule(callback: CallbackQuery, state: FSMContext):
    token = await require_token(callback)
    if not token:
        await callback.answer()
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/workouts/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code != 200:
        await callback.message.answer("❌ Не удалось получить тренировки.")
        await callback.answer()
        return

    workouts = response.json()

    if not workouts:
        await callback.message.answer("Сначала создай тренировку.")
        await callback.answer()
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=workout["name"],
                    callback_data=f"schedule_workout_{workout['id']}",
                )
            ]
            for workout in workouts
        ]
    )

    await callback.message.answer("Выбери тренировку:", reply_markup=kb)
    await state.set_state(ScheduleStates.waiting_workout)
    await callback.answer()


@router.callback_query(ScheduleStates.waiting_workout)
async def process_schedule_workout(callback: CallbackQuery, state: FSMContext):
    workout_id = int(callback.data.replace("schedule_workout_", ""))

    await state.update_data(workout_id=workout_id)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=name,
                    callback_data=f"schedule_weekday_{number}",
                )
            ]
            for number, name in WEEKDAYS.items()
        ]
    )

    await callback.message.answer("Выбери день недели:", reply_markup=kb)
    await state.set_state(ScheduleStates.waiting_weekday)
    await callback.answer()


@router.callback_query(ScheduleStates.waiting_weekday)
async def process_schedule_weekday(callback: CallbackQuery, state: FSMContext):
    weekday = int(callback.data.replace("schedule_weekday_", ""))

    await state.update_data(weekday=weekday)
    await callback.message.answer("Введи время тренировки в формате HH:MM")
    await state.set_state(ScheduleStates.waiting_time)
    await callback.answer()


@router.message(ScheduleStates.waiting_time)
async def process_schedule_time(message: Message, state: FSMContext):
    workout_time = message.text.strip()

    try:
        hours, minutes = map(int, workout_time.split(":"))
    except ValueError:
        await message.answer("Введи время в формате HH:MM, например 18:30")
        return

    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        await message.answer("Введи корректное время, например 18:30")
        return

    await state.update_data(workout_time=f"{hours:02d}:{minutes:02d}")
    await message.answer(
        "За сколько минут напомнить?",
        reply_markup=reminder_minutes_keyboard,
    )
    await state.set_state(ScheduleStates.waiting_reminder_minutes)


@router.callback_query(ScheduleStates.waiting_reminder_minutes)
async def process_reminder_minutes(callback: CallbackQuery, state: FSMContext):
    token = await require_token(callback)
    if not token:
        await callback.answer()
        await state.clear()
        return

    reminder_minutes = int(callback.data.replace("reminder_", ""))

    data = await state.get_data()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/workout-schedules/schedules/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "workout_id": data["workout_id"],
                "weekday": data["weekday"],
                "workout_time": data["workout_time"],
                "reminder_minutes_before": reminder_minutes,
            },
        )

    if response.status_code in (200, 201):
        await callback.message.answer("✅ Напоминание создано!")
    else:
        await callback.message.answer("❌ Не удалось создать напоминание.")

    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "schedules_delete")
async def start_delete_schedule(callback: CallbackQuery):
    token = await require_token(callback)
    if not token:
        await callback.answer()
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/workout-schedules/schedules/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if response.status_code != 200:
        await callback.message.answer("❌ Не удалось получить напоминания.")
        await callback.answer()
        return

    schedules = response.json()

    if not schedules:
        await callback.message.answer("У тебя пока нет напоминаний.")
        await callback.answer()
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"{WEEKDAYS.get(schedule['weekday'], 'День')} "
                        f"{schedule['workout_time']}"
                    ),
                    callback_data=f"delete_schedule_{schedule['id']}",
                )
            ]
            for schedule in schedules
        ]
    )

    await callback.message.answer(
        "Выбери напоминание для удаления:",
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(F.data == "schedules_delete")
async def start_delete_schedule(callback: CallbackQuery):
    token = await require_token(callback)
    if not token:
        await callback.answer()
        return

    async with httpx.AsyncClient() as client:
        schedules_response = await client.get(
            f"{API_URL}/workout-schedules/schedules/",
            headers={"Authorization": f"Bearer {token}"},
        )

        workouts_response = await client.get(
            f"{API_URL}/workouts/",
            headers={"Authorization": f"Bearer {token}"},
        )

    if schedules_response.status_code != 200:
        await callback.message.answer("❌ Не удалось получить напоминания.")
        await callback.answer()
        return

    schedules = schedules_response.json()

    if not schedules:
        await callback.message.answer("У тебя пока нет напоминаний.")
        await callback.answer()
        return

    workouts_by_id = {}

    if workouts_response.status_code == 200:
        workouts_by_id = {
            workout["id"]: workout["name"] for workout in workouts_response.json()
        }

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=(
                        f"{workouts_by_id.get(schedule['workout_id'], 'Тренировка')} — "
                        f"{WEEKDAYS.get(schedule['weekday'], 'День')} "
                        f"{schedule['workout_time']}"
                    ),
                    callback_data=f"delete_schedule_{schedule['id']}",
                )
            ]
            for schedule in schedules
        ]
    )

    await callback.message.answer(
        "Выбери напоминание для удаления:",
        reply_markup=kb,
    )
    await callback.answer()
