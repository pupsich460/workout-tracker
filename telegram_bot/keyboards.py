from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💪 Мои тренировки")],
        [KeyboardButton(text="➕ Создать тренировку")],
        [KeyboardButton(text="🤖 Сгенерировать тренировку")],
        [KeyboardButton(text="📝 Отметить тренировку")],
        [KeyboardButton(text="🔑 Войти")],
    ],
    resize_keyboard=True,
)

level_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Новичок", callback_data="Новичок")],
        [InlineKeyboardButton(text="🟡 Средний", callback_data="Промежуточный")],
        [InlineKeyboardButton(text="🔴 Продвинутый", callback_data="Продвинутый")],
    ]
)
