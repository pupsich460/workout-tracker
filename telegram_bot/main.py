import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.core.config import settings
from telegram_bot.routers import auth, generate, logs, workouts

bot = Bot(token=settings.bot_token)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(auth.router)
dp.include_router(workouts.router)
dp.include_router(generate.router)
dp.include_router(logs.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
