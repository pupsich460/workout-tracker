import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)

async def _send_telegram_message(telegram_id: int, text: str):
    bot = Bot(token=settings.bot_token)

    try:
        await bot.send_message(chat_id=telegram_id, text=text)
    except TelegramBadRequest as e:
        logger.error("Telegram bad request for chat_id=%s: %s", telegram_id, e)
        raise
    except TelegramForbiddenError as e:
        logger.error("Telegram forbidden for chat_id=%s: %s", telegram_id, e)
        raise

    finally:
        await bot.session.close()


@celery_app.task
def send_workout_reminder(telegram_id: int, text: str):
    asyncio.run(_send_telegram_message(telegram_id, text))
