import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from app.core.config import settings
from app.core.redis import redis_client
from telegram_bot.routers import (
    auth,
    common,
    generate,
    logs,
    logs_history,
    schedules,
    workouts,
)

bot = Bot(token=settings.bot_token)
dp = Dispatcher(storage=RedisStorage(redis=redis_client))

dp.include_router(auth.router)
dp.include_router(workouts.router)
dp.include_router(generate.router)
dp.include_router(logs.router)
dp.include_router(logs_history.router)
dp.include_router(common.router)
dp.include_router(schedules.router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
