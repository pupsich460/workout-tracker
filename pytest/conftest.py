import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.db import Base, get_async_session
from app.main import app

# Используем отдельную in-memory БД для тестов — не трогаем рабочую
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_async_session():
    async with TestSessionLocal() as session:
        yield session


# Подменяем зависимость сессии на тестовую
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    """Создаёт таблицы перед каждым тестом и удаляет после."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():
    """HTTP-клиент для запросов к приложению."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def registered_user(client):
    """Зарегистрированный пользователь."""
    await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass",
        },
    )
    return {"email": "test@example.com", "password": "testpass"}


@pytest_asyncio.fixture
async def auth_headers(client, registered_user):
    """Заголовки с JWT-токеном для авторизованных запросов."""
    response = await client.post(
        "/auth/jwt/login",
        data={
            "username": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def workout(client, auth_headers):
    """Созданная тренировка."""
    response = await client.post(
        "/workouts/",
        json={
            "name": "Тестовая тренировка",
            "description": "Описание",
        },
        headers=auth_headers,
    )
    return response.json()


@pytest_asyncio.fixture
async def exercise(client, auth_headers):
    """Созданное упражнение."""
    response = await client.post(
        "/exercises/",
        json={
            "name": "Жим лёжа",
            "description": "Базовое упражнение",
        },
        headers=auth_headers,
    )
    return response.json()
