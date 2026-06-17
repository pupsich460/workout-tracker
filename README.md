# 🏋️ Workout Tracker API

FastAPI-приложение для трекинга тренировок с Telegram-ботом, AI-генерацией тренировок и системой напоминаний.

**Live demo:** [workouttracker.accesscam.org](https://workouttracker.accesscam.org)

## Возможности

- Регистрация и аутентификация пользователей (JWT через fastapi-users)
- CRUD для тренировок, упражнений и логов тренировок
- Добавление упражнений в тренировки с указанием подходов и повторений
- Расписание тренировок с напоминаниями
- Генерация тренировок через AI
- Telegram-бот (aiogram 3) — управление тренировками, логирование, AI-генерация
- Асинхронный стек: FastAPI + SQLAlchemy (async) + PostgreSQL
- Celery + Redis для фоновых задач и напоминаний

## Стек

| Слой | Технологии |
|---|---|
| API | FastAPI, fastapi-users |
| База данных | PostgreSQL, SQLAlchemy (async), Alembic |
| Фоновые задачи | Celery, Redis |
| Telegram-бот | aiogram 3 |
| AI | Groq API |
| Тесты | pytest, pytest-asyncio, pytest-cov |
| Линтер | Ruff |
| Контейнеризация | Docker, Docker Compose |
| CI/CD | GitHub Actions → Docker Hub → VPS |

## Быстрый старт

### Локально (для разработки)

```bash
git clone https://github.com/pupsich460/workout-tracker.git
cd workout-tracker
cp .env.example .env  # заполни переменные
docker compose up -d
docker compose exec backend alembic upgrade head
```

API будет доступно на `http://localhost:8000`.  
Документация: `http://localhost:8000/docs`.

### Production

```bash
docker compose -f docker-compose.production.yml pull
docker compose -f docker-compose.production.yml up -d
docker compose -f docker-compose.production.yml exec backend alembic upgrade head
```

## Переменные окружения

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tracker_db
DB_USER=postgres
DB_PASSWORD=postgres
SECRET=your-secret-key
GROQ_API_KEY=your-groq-api-key
BOT_TOKEN=your-telegram-bot-token
API_URL=http://backend:8000
REDIS_HOST=redis
REDIS_PORT=6379
SQL_ECHO=false
```

## API — основные эндпоинты

### Аутентификация
| Метод | URL | Описание |
|---|---|---|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/jwt/login` | Вход, получение токена |

### Тренировки
| Метод | URL | Описание |
|---|---|---|
| GET | `/workouts/` | Список тренировок |
| POST | `/workouts/` | Создать тренировку |
| GET | `/workouts/{id}` | Получить тренировку |
| PATCH | `/workouts/{id}` | Обновить тренировку |
| DELETE | `/workouts/{id}` | Удалить тренировку |
| GET | `/workouts/{id}/exercises` | Упражнения в тренировке |
| POST | `/workouts/{id}/exercises` | Добавить упражнение в тренировку |
| DELETE | `/workouts/{id}/exercises/{ex_id}` | Удалить упражнение из тренировки |
| POST | `/workouts/ai/generate` | AI-генерация тренировки |

### Упражнения
| Метод | URL | Описание |
|---|---|---|
| GET | `/exercises/` | Список упражнений |
| POST | `/exercises/` | Создать упражнение |
| GET | `/exercises/{id}` | Получить упражнение |
| PATCH | `/exercises/{id}` | Обновить упражнение |
| DELETE | `/exercises/{id}` | Удалить упражнение |

### Логи тренировок
| Метод | URL | Описание |
|---|---|---|
| GET | `/workout-logs/` | Список логов |
| POST | `/workout-logs/` | Отметить тренировку выполненной |
| GET | `/workout-logs/{id}` | Получить лог |
| PATCH | `/workout-logs/{id}` | Обновить лог |
| DELETE | `/workout-logs/{id}` | Удалить лог |

### Расписание
| Метод | URL | Описание |
|---|---|---|
| GET | `/workout-schedules/schedules/` | Список расписаний |
| POST | `/workout-schedules/schedules/` | Создать расписание |
| DELETE | `/workout-schedules/schedules/{id}` | Удалить расписание |

## Тесты

```bash
# Запустить все тесты с покрытием
PYTHONPATH=. pytest --cov=app --cov=telegram_bot --cov-report=term

# Только API-тесты
PYTHONPATH=. pytest pytest/test_workouts.py pytest/test_exercises.py pytest/test_workout_logs.py -v
```

## CI/CD

GitHub Actions запускает при каждом push в `master`:

1. **Проверки** — `ruff format`, `ruff check`, тесты с покрытием
2. **Сборка** — Docker-образ публикуется на Docker Hub
3. **Деплой** — автоматический деплой на VPS через SSH

### Secrets (GitHub → Settings → Secrets and variables → Actions)

| Secret | Описание |
|---|---|
| `DOCKER_USERNAME` | Логин на Docker Hub |
| `DOCKER_PASSWORD` | Пароль или Access Token Docker Hub |
| `HOST` | IP-адрес или домен VPS |
| `USER` | SSH-пользователь на VPS (например, `root`) |
| `SSH_KEY` | Приватный SSH-ключ для подключения к VPS |

## Структура проекта

```
workout-tracker/
├── app/
│   ├── api/v1/endpoints/   # FastAPI роутеры
│   ├── core/               # Конфиг, БД, зависимости, пользователи
│   ├── crud/               # CRUD-операции
│   ├── models/             # SQLAlchemy модели
│   ├── schemas/            # Pydantic схемы
│   ├── services/           # AI-генерация тренировок
│   └── tasks/              # Celery задачи
├── telegram_bot/
│   ├── routers/            # Хендлеры aiogram
│   ├── services/           # Логика бота
│   └── states.py           # FSM состояния
├── pytest/                 # Тесты
├── docker-compose.yml
├── docker-compose.production.yml
└── Dockerfile
```