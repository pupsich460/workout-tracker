import importlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram.types import Chat, Message, User


def make_message(text: str, user_id: int = 123456) -> MagicMock:
    message = MagicMock(spec=Message)
    message.text = text
    message.answer = AsyncMock()
    message.from_user = MagicMock(spec=User)
    message.from_user.id = user_id
    message.chat = MagicMock(spec=Chat)
    message.chat.id = 1
    return message


@pytest.mark.asyncio
async def test_cmd_start():
    import telegram_bot.routers.auth as am
    importlib.reload(am)

    message = make_message("/start")
    await am.cmd_start(message)
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_cmd_link_no_code():
    import telegram_bot.routers.auth as am
    importlib.reload(am)

    message = make_message("/link")
    await am.cmd_link(message)
    message.answer.assert_called()


@pytest.mark.asyncio
async def test_cmd_cancel_no_state():
    import telegram_bot.routers.common as cm
    importlib.reload(cm)

    state = AsyncMock()
    state.get_state = AsyncMock(return_value=None)

    message = make_message("/cancel")
    await cm.cancel_handler(message, state)
    message.answer.assert_called_with("Нечего отменять.")


class TestWorkoutsBot:
    @pytest.mark.asyncio
    async def test_get_workouts_no_token(self):
        import telegram_bot.routers.workouts as wm
        importlib.reload(wm)

        # require_token сама вызывает answer на message и возвращает None
        # поэтому патчим так, чтобы она вызвала answer и вернула None
        async def fake_require_token(msg):
            await msg.answer("Сначала привяжи аккаунт через /link CODE")
            return None

        with patch.object(wm, "require_token", new=fake_require_token):
            message = make_message("💪 Мои тренировки")
            await wm.get_workouts(message)
            message.answer.assert_called()

    @pytest.mark.asyncio
    async def test_get_workouts_empty(self):
        import telegram_bot.routers.workouts as wm
        importlib.reload(wm)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get.return_value = mock_response

        with patch.object(wm, "require_token", new=AsyncMock(return_value="test-token")), \
             patch.object(wm.httpx, "AsyncClient", return_value=mock_client):
            message = make_message("💪 Мои тренировки")
            await wm.get_workouts(message)
            message.answer.assert_called()

    @pytest.mark.asyncio
    async def test_get_workouts_with_data(self):
        import telegram_bot.routers.workouts as wm
        importlib.reload(wm)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "Силовая", "description": "Тест"}
        ]

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get.return_value = mock_response

        with patch.object(wm, "require_token", new=AsyncMock(return_value="test-token")), \
             patch.object(wm.httpx, "AsyncClient", return_value=mock_client):
            message = make_message("💪 Мои тренировки")
            await wm.get_workouts(message)
            message.answer.assert_called()


class TestLogsBot:
    @pytest.mark.asyncio
    async def test_log_no_token(self):
        import telegram_bot.routers.logs as lm
        importlib.reload(lm)

        async def fake_require_token(msg):
            await msg.answer("Сначала привяжи аккаунт через /link CODE")
            return None

        with patch.object(lm, "require_token", new=fake_require_token):
            message = make_message("📝 Отметить тренировку")
            await lm.cmd_log(message)
            message.answer.assert_called()

    @pytest.mark.asyncio
    async def test_log_no_workouts(self):
        import telegram_bot.routers.logs as lm
        importlib.reload(lm)

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get.return_value = mock_response

        with patch.object(lm, "require_token", new=AsyncMock(return_value="test-token")), \
             patch.object(lm.httpx, "AsyncClient", return_value=mock_client):
            message = make_message("📝 Отметить тренировку")
            await lm.cmd_log(message)
            message.answer.assert_called()
