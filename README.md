# 🏋️ Workout Tracker

REST API для трекинга тренировок с AI-генерацией планов и Telegram ботом.

## Возможности

- Регистрация и аутентификация пользователей (JWT)
- Создание и управление тренировками и упражнениями
- Добавление упражнений в тренировки с указанием подходов и повторений
- Логирование выполненных тренировок
- **AI-генерация тренировки** на основе цели, уровня подготовки и веса пользователя
- **Telegram бот** с полным функционалом приложения

## Стек

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — основной фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) (async) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — миграции БД
- [Pydantic v2](https://docs.pydantic.dev/) — валидация данных
- [fastapi-users](https://fastapi-users.github.io/fastapi-users/) — аутентификация и управление пользователями

**Telegram бот**
- [aiogram 3](https://docs.aiogram.dev/) — async фреймворк для Telegram ботов
- FSM (Finite State Machine) — многошаговые диалоги

**AI**
- [Groq API](https://groq.com/) — LLM inference (llama-3.3-70b-versatile)

**Инфраструктура**
- SQLite (dev) / совместимо с PostgreSQL
- [httpx](https://www.python-httpx.org/) — async HTTP клиент
- [uvicorn](https://www.uvicorn.org/) — ASGI сервер
- [Docker](https://www.docker.com/) — контейнеризация

## Запуск через Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com/pupsich460/workout-tracker.git
cd workout-tracker

# Создать .env файл
cp .env.example .env
# Заполнить переменные в .env

# Запустить
docker-compose up --build
```

API будет доступен на `http://localhost:8000/docs`

## Локальный запуск

```bash
# Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
cp .env.example .env
# Заполнить переменные в .env

# Применить миграции
alembic upgrade head

# Запустить API
uvicorn app.main:app --reload

# Запустить бота (в отдельном терминале)
python -m telegram_bot.main
```

## Переменные окружения

Создай файл `.env` на основе `.env.example`:

```
APP_TITLE=Workout Tracker
DATABASE_URL=sqlite+aiosqlite:///./tracker.db
SECRET=your_secret_key
BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
API_URL=http://127.0.0.1:8000  # локально
# API_URL=http://api:8000       # в Docker
```

## Структура проекта

```
├── app/
│   ├── api/
│   │   ├── endpoints/      # Роутеры (exercise, workout, workout_logs, users)
│   │   └── validators.py   # Общие валидаторы
│   ├── core/
│   │   ├── config.py       # Настройки приложения
│   │   ├── db.py           # Подключение к БД
│   │   └── user.py         # Настройка fastapi-users
│   ├── crud/               # CRUD операции
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   ├── services/
│   │   └── ai_workout.py   # Генерация тренировок через LLM
│   └── main.py
├── telegram_bot/
│   ├── routers/
│   │   ├── auth.py         # Авторизация
│   │   ├── workouts.py     # Управление тренировками
│   │   ├── generate.py     # AI-генерация
│   │   └── logs.py         # Логи тренировок
│   ├── keyboards.py
│   ├── states.py
│   ├── storage.py
│   └── main.py
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## API Endpoints

После запуска документация доступна по адресу: `http://127.0.0.1:8000/docs`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/jwt/login` | Получить JWT токен |
| GET | `/exercises/` | Список упражнений |
| POST | `/exercises/` | Создать упражнение |
| GET | `/workouts/` | Список тренировок |
| POST | `/workouts/` | Создать тренировку |
| POST | `/workouts/generate` | **AI-генерация тренировки** |
| POST | `/workouts/{id}/exercises` | Добавить упражнение в тренировку |
| DELETE | `/workouts/{id}/exercises/{exercise_id}` | Удалить упражнение из тренировки |
| DELETE | `/workouts/{id}` | Удалить тренировку |
| GET | `/workout-logs/` | Список логов |
| POST | `/workout-logs/` | Отметить тренировку выполненной |
| POST | `/users/link-telegram` | Привязать Telegram аккаунт |

## Telegram бот

Бот поддерживает полный функционал приложения:
- Авторизация через email + пароль
- Просмотр списка тренировок
- Создание тренировок вручную
- AI-генерация тренировки по параметрам
- Добавление упражнений в тренировку
- Отметить тренировку выполненной
- Удаление тренировок