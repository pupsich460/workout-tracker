from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is None:
        await message.answer("Нечего отменять.")
        return

    await state.clear()
    await message.answer("❌ Текущее действие отменено.")
