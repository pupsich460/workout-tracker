# 🏋️ Workout Tracker API

REST API для трекинга тренировок с AI-генерацией планов на основе целей пользователя.

## Возможности

- Регистрация и аутентификация пользователей (JWT)
- Создание и управление тренировками и упражнениями
- Добавление упражнений в тренировки с указанием подходов и повторений
- Логирование выполненных тренировок
- **AI-генерация тренировки** на основе цели, уровня подготовки и веса пользователя

## Стек

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — основной фреймворк
- [SQLAlchemy](https://www.sqlalchemy.org/) (async) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — миграции БД
- [Pydantic v2](https://docs.pydantic.dev/) — валидация данных
- [fastapi-users](https://fastapi-users.github.io/fastapi-users/) — аутентификация и управление пользователями

**AI**
- [Groq API](https://groq.com/) — LLM inference (llama-3.3-70b-versatile)

**Инфраструктура**
- SQLite (dev) / совместимо с PostgreSQL
- [httpx](https://www.python-httpx.org/) — async HTTP клиент
- [uvicorn](https://www.uvicorn.org/) — ASGI сервер

## Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/твой_юзернейм/workout-tracker.git
cd workout-tracker

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

# Запустить сервер
uvicorn app.main:app --reload
```

## Переменные окружения

Создай файл `.env` в корне проекта:

```
APP_TITLE=Workout Tracker
DATABASE_URL=sqlite+aiosqlite:///./workout_tracker.db
SECRET=your_secret_key
GROQ_API_KEY=your_groq_api_key
```

## Структура проекта

```
app/
├── api/
│   ├── endpoints/      # Роутеры (exercise, workout, workout_logs, user)
│   └── validators.py   # Общие валидаторы
├── core/
│   ├── config.py       # Настройки приложения
│   ├── db.py           # Подключение к БД
│   └── user.py         # Настройка fastapi-users
├── crud/               # CRUD операции
├── models/             # SQLAlchemy модели
├── schemas/            # Pydantic схемы
├── services/
│   └── ai_workout.py   # Генерация тренировок через LLM
└── main.py
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
| GET | `/workout-logs/` | Список логов |
| POST | `/workout-logs/` | Отметить тренировку выполненной |