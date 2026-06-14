from unittest.mock import AsyncMock, patch

from aiogram import Dispatcher
from aiogram.types import Chat, Message, Update, User

import pytest
from telegram_bot.routers import auth, common, logs, workouts


def make_message(text: str, user_id: int = 123456) -> Message:
    return Message(
        message_id=1,
        date=1,
        chat=Chat(id=1, type="private"),
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        text=text,
    )


def make_callback_query(data: str, user_id: int = 123456):
    from aiogram.types import CallbackQuery

    return CallbackQuery(
        id="1",
        from_user=User(id=user_id, is_bot=False, first_name="Test"),
        chat_instance="1",
        data=data,
        message=Message(
            message_id=1,
            date=1,
            chat=Chat(id=1, type="private"),
            from_user=User(id=user_id, is_bot=False, first_name="Test"),
            text="test",
        ),
    )


@pytest.fixture
def dp():
    dispatcher = Dispatcher()
    dispatcher.include_router(auth.router)
    dispatcher.include_router(workouts.router)
    dispatcher.include_router(logs.router)
    dispatcher.include_router(common.router)
    return dispatcher


@pytest.mark.asyncio
async def test_cmd_start(dp):
    message = make_message("/start")
    await dp.feed_update(
        bot=AsyncMock(),
        update=Update(message=message, update_id=1),
    )
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_cmd_link_no_code(dp):
    message = make_message("/link")
    await dp.feed_update(
        bot=AsyncMock(),
        update=Update(message=message, update_id=1),
    )
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_cmd_cancel_no_state(dp):
    message = make_message("/cancel")
    await dp.feed_update(
        bot=AsyncMock(),
        update=Update(message=message, update_id=1),
    )
    message.answer.assert_called()


class TestWorkoutsBot:
    @patch("telegram_bot.routers.workouts.require_token")
    async def test_get_workouts_no_token(self, mock_require_token, dp):
        mock_require_token.return_value = None
        message = make_message("💪 Мои тренировки")
        await dp.feed_update(
            bot=AsyncMock(),
            update=Update(message=message, update_id=1),
        )
        message.answer.assert_called()

    @patch("telegram_bot.routers.workouts.require_token")
    @patch("telegram_bot.routers.workouts.httpx.AsyncClient")
    async def test_get_workouts_empty(self, mock_client_cls, mock_require_token, dp):
        mock_require_token.return_value = "test-token"

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value = mock_client

        message = make_message("💪 Мои тренировки")
        await dp.feed_update(
            bot=AsyncMock(),
            update=Update(message=message, update_id=1),
        )
        message.answer.assert_called()

    @patch("telegram_bot.routers.workouts.require_token")
    @patch("telegram_bot.routers.workouts.httpx.AsyncClient")
    async def test_get_workouts_with_data(
        self, mock_client_cls, mock_require_token, dp
    ):
        mock_require_token.return_value = "test-token"

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "Силовая", "description": "Тест"}
        ]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value = mock_client

        message = make_message("💪 Мои тренировки")
        await dp.feed_update(
            bot=AsyncMock(),
            update=Update(message=message, update_id=1),
        )
        message.answer.assert_called()


class TestLogsBot:
    @patch("telegram_bot.routers.logs.require_token")
    async def test_log_no_token(self, mock_require_token, dp):
        mock_require_token.return_value = None
        message = make_message("📝 Отметить тренировку")
        await dp.feed_update(
            bot=AsyncMock(),
            update=Update(message=message, update_id=1),
        )
        message.answer.assert_called()

    @patch("telegram_bot.routers.logs.require_token")
    @patch("telegram_bot.routers.logs.httpx.AsyncClient")
    async def test_log_no_workouts(self, mock_client_cls, mock_require_token, dp):
        mock_require_token.return_value = "test-token"

        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value = mock_client

        message = make_message("📝 Отметить тренировку")
        await dp.feed_update(
            bot=AsyncMock(),
            update=Update(message=message, update_id=1),
        )
        message.answer.assert_called()
