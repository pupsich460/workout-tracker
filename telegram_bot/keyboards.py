from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💪 Мои тренировки")],
        [KeyboardButton(text="➕ Создать тренировку")],
        [KeyboardButton(text="🤖 Сгенерировать тренировку")],
        [KeyboardButton(text="⏰ Напоминания")],
        [KeyboardButton(text="📝 Отметить тренировку")],
        [KeyboardButton(text="📊 История тренировок")],
        [KeyboardButton(text="🔗 Привязать аккаунт")],
        [KeyboardButton(text=" 🔑 Авторизоваться")],
    ],
    resize_keyboard=True,
)

goal_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔥 Похудеть", callback_data="goal_Похудеть")],
        [
            InlineKeyboardButton(
                text="💪 Набрать массу", callback_data="goal_Набрать массу"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚖️ Поддерживать форму", callback_data="goal_Поддерживать форму"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏃 Выносливость", callback_data="goal_Выносливость"
            )
        ],
        [
            InlineKeyboardButton(
                text="🧘 Общее здоровье", callback_data="goal_Общее здоровье"
            )
        ],
    ]
)

level_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Новичок", callback_data="level_Новичок")],
        [InlineKeyboardButton(text="🟡 Средний", callback_data="level_Промежуточный")],
        [
            InlineKeyboardButton(
                text="🔴 Продвинутый", callback_data="level_Продвинутый"
            )
        ],
    ]
)


reminder_minutes_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="15 мин", callback_data="reminder_15"),
            InlineKeyboardButton(text="30 мин", callback_data="reminder_30"),
        ],
        [
            InlineKeyboardButton(text="60 мин", callback_data="reminder_60"),
            InlineKeyboardButton(text="120 мин", callback_data="reminder_120"),
        ],
    ]
)
