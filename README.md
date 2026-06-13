# 🏋️ Workout Tracker API

REST API и Telegram-бот для управления тренировками, планирования занятий, ведения истории тренировок и автоматизации фитнес-процессов.

Проект построен на **FastAPI** и включает:

* JWT-аутентификацию
* PostgreSQL
* Redis
* Celery Worker
* Celery Beat
* Flower Monitoring
* Telegram Bot на Aiogram 3
* AI-генерацию тренировок через Groq
* Docker и Docker Compose
* GitHub Actions CI/CD
* Автоматическую публикацию Docker-образов в Docker Hub
* Автоматический деплой на VPS

---

# 🚀 Features

## Authentication

* Регистрация пользователей
* JWT-аутентификация
* Защищённые эндпоинты
* Привязка Telegram аккаунта через одноразовый код
* Автоматическая авторизация Telegram-пользователей

## Exercises

* Создание упражнений
* Редактирование упражнений
* Удаление упражнений
* Просмотр списка упражнений

## Workouts

* Создание тренировок
* Редактирование тренировок
* Удаление тренировок
* Добавление упражнений в тренировку
* Просмотр тренировок пользователя

## Workout Logs

* Ведение истории тренировок
* Отслеживание выполненных тренировок

## Workout Schedule

* Создание расписания тренировок
* Просмотр расписания
* Удаление расписания
* Планирование тренировок по дням недели

## Notifications

* Автоматические напоминания о тренировках
* Отправка уведомлений через Telegram
* Celery Beat для запуска планировщика
* Celery Worker для обработки фоновых задач

## Telegram Bot

* Привязка Telegram аккаунта
* Автоматическая авторизация по Telegram ID
* Просмотр тренировок
* Создание тренировок
* Удаление тренировок
* Добавление упражнений
* Логирование выполненных тренировок
* Создание расписания тренировок
* Просмотр расписания
* Удаление расписания
* AI-генерация тренировочных программ
* Получение автоматических напоминаний

## AI Integration

* Генерация тренировок через Groq API
* Использование модели Llama 3.3 70B Versatile
* Формирование тренировочного плана на основе параметров пользователя

## Monitoring

* Flower для мониторинга Celery задач
* Просмотр активных задач
* Просмотр очередей
* Мониторинг воркеров

---

# 🏗 Architecture

```text
Telegram Bot (Aiogram)
            │
            ▼
      FastAPI Backend
            │
 ┌──────────┴──────────┐
 ▼                     ▼
PostgreSQL           Redis
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Celery Worker           Celery Beat
             │
             ▼
 Telegram Notifications
```

---

# 🛠 Tech Stack

## Backend

* FastAPI
* SQLAlchemy Async
* PostgreSQL
* Alembic
* Pydantic v2
* FastAPI Users

## Background Tasks

* Redis
* Celery
* Celery Beat
* Flower

## Telegram Bot

* Aiogram 3
* FSM

## AI

* Groq API
* Llama 3.3 70B Versatile

## Testing

* Pytest
* Pytest Asyncio
* Pytest Cov

## DevOps

* Docker
* Docker Compose
* GitHub Actions
* Docker Hub
* VPS Deployment

---

# 📁 Project Structure

```text
.
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── crud/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   └── main.py
├── telegram_bot/
├── pytest/
├── .github/
│   └── workflows/
├── Dockerfile
├── docker-compose.production.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Environment Variables

Создай файл `.env` на основе `.env.example`.

Пример:

```env
APP_TITLE=Workout Tracker API

SECRET=

GROQ_API_KEY=
BOT_TOKEN=

API_URL=http://backend:8000

DB_HOST=db
DB_PORT=5432
DB_NAME=tracker_db
DB_USER=postgres
DB_PASSWORD=postgres

REDIS_HOST=redis
REDIS_PORT=6379
```

---

# 🐳 Docker

Сборка образа:

```bash
docker build -t workout-tracker-api .
```

Запуск контейнера:

```bash
docker run -p 8000:8000 workout-tracker-api
```

---

# 🐳 Docker Compose

Production окружение включает:

* Backend API
* PostgreSQL
* Redis
* Celery Worker
* Celery Beat
* Flower
* Telegram Bot

Запуск:

```bash
docker compose -f docker-compose.production.yml up -d
```

Остановка:

```bash
docker compose -f docker-compose.production.yml down
```

Просмотр логов:

```bash
docker compose -f docker-compose.production.yml logs -f
```

---

# 🌼 Flower Monitoring

После запуска:

```text
http://SERVER_IP:5555
```

Доступны:

* Active Tasks
* Scheduled Tasks
* Workers
* Queues
* Task History

---

# 🗄 Database Migrations

Создать миграцию:

```bash
alembic revision --autogenerate -m "migration_name"
```

Применить миграции:

```bash
alembic upgrade head
```

---

# 🧪 Testing

Запуск тестов:

```bash
pytest
```

Покрытие:

```bash
pytest --cov=app
```

---

# 🔍 Code Quality

Форматирование:

```bash
black .
```

Сортировка импортов:

```bash
isort .
```

Проверка:

```bash
black --check .
isort --check-only .
```

---

# 🤖 Telegram Bot

Основное меню:

```text
💪 Мои тренировки
➕ Создать тренировку
🤖 Сгенерировать тренировку
📝 Отметить тренировку
⏰ Напоминания
```

Поддерживаемые функции:

* Просмотр тренировок
* Создание тренировок
* Удаление тренировок
* Добавление упражнений
* Логирование тренировок
* Создание расписания
* Просмотр расписания
* Удаление расписания
* AI-генерация тренировок
* Автоматические напоминания

---

# 🔄 CI/CD

GitHub Actions автоматически выполняет:

* Проверку Black
* Проверку isort
* Запуск Pytest
* Сборку Docker-образа
* Публикацию Docker-образа в Docker Hub
* Автоматический деплой на VPS
* Применение миграций базы данных

Workflow запускается при:

* Push в `master`
* Pull Request в `master`

---

# 🔐 GitHub Secrets

Для работы CI/CD необходимо добавить следующие секреты:

## Docker Hub

| Secret          | Description             |
| --------------- | ----------------------- |
| DOCKER_USERNAME | Docker Hub username     |
| DOCKER_PASSWORD | Docker Hub access token |

## VPS Deployment

| Secret  | Description        |
| ------- | ------------------ |
| HOST    | IP адрес сервера   |
| USER    | SSH пользователь   |
| SSH_KEY | Приватный SSH ключ |

---

# 🐋 Docker Hub

Образ проекта:

```bash
docker pull pupsich460/workout-tracker-api:latest
```

---

# 📚 API Documentation

После запуска приложения:

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 📌 Main Endpoints

# 📌 Main Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | `/auth/register` | User registration |
| POST | `/auth/jwt/login` | JWT login |
| GET | `/exercises/` | List exercises |
| POST | `/exercises/` | Create exercise |
| GET | `/workouts/` | List workouts |
| POST | `/workouts/` | Create workout |
| GET | `/workouts/{workout_id}` | Get workout detail |
| DELETE | `/workouts/{workout_id}` | Delete workout |
| POST | `/workouts/{workout_id}/exercises` | Add exercise to workout |
| DELETE | `/workouts/{workout_id}/exercises/{exercise_id}` | Remove exercise from workout |
| POST | `/workouts/ai/generate` | Generate workout with AI |
| GET | `/workout-logs/` | List workout logs |
| POST | `/workout-logs/` | Create workout log |
| POST | `/telegram/link-code` | Generate Telegram link code |
| POST | `/telegram/link` | Link Telegram account by code |
| POST | `/telegram/auth` | Authenticate Telegram user |
| GET | `/workout-schedules/schedules/` | List workout schedules |
| POST | `/workout-schedules/schedules/` | Create workout schedule |
| PATCH | `/workout-schedules/schedules/{schedule_id}/deactivate` | Deactivate workout schedule |
| DELETE | `/workout-schedules/schedules/{schedule_id}` | Delete workout schedule |

---

# 🎯 Project Goals

* Практика построения production-ready FastAPI приложения
* Работа с PostgreSQL и SQLAlchemy Async
* Интеграция Redis и Celery
* Интеграция Telegram Bot
* Интеграция AI сервисов
* Настройка CI/CD пайплайна
* Контейнеризация приложения через Docker
* Автоматический деплой на VPS

---
