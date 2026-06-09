# 🏋️ Workout Tracker API

REST API для управления тренировками, ведения истории занятий и автоматизации фитнес-процессов.

Проект построен на **FastAPI** и включает:

* JWT-аутентификацию
* PostgreSQL
* Redis + Celery
* Telegram Bot
* AI-генерацию тренировок через Groq
* Docker и Docker Compose
* GitHub Actions CI/CD
* Автоматическую публикацию Docker-образов в Docker Hub

---

## 🚀 Features

### Authentication

* Регистрация пользователей
* JWT-аутентификация
* Защищённые эндпоинты

### Exercises

* Создание упражнений
* Редактирование упражнений
* Удаление упражнений
* Просмотр списка упражнений

### Workouts

* Создание тренировок
* Добавление упражнений
* Редактирование тренировок
* Удаление тренировок

### Workout Logs

* Ведение истории тренировок
* Отслеживание выполнения тренировок

### Workout Schedule

* Планирование тренировок
* Хранение расписания пользователя

### Telegram Bot

* Авторизация через API
* Просмотр тренировок
* Создание тренировок
* Логирование тренировок
* AI-генерация тренировочных программ

### AI Integration

* Генерация тренировок через Groq API
* Формирование плана на основе параметров пользователя

---

## 🛠 Tech Stack

### Backend

* FastAPI
* SQLAlchemy Async
* PostgreSQL
* Alembic
* Pydantic v2
* FastAPI Users

### Background Tasks

* Redis
* Celery

### Telegram Bot

* Aiogram 3
* FSM

### AI

* Groq API
* Llama 3.3 70B Versatile

### Testing

* Pytest
* Pytest Asyncio
* Pytest Cov

### DevOps

* Docker
* Docker Compose
* GitHub Actions
* Docker Hub

---

## 📁 Project Structure

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

## ⚙️ Environment Variables

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

## 🐳 Docker

Сборка образа:

```bash
docker build -t workout-tracker-api .
```

Запуск контейнера:

```bash
docker run -p 8000:8000 workout-tracker-api
```

---

## 🐳 Docker Compose

Production окружение включает:

* Backend API
* PostgreSQL
* Redis
* Celery Worker
* Telegram Bot

Запуск:

```bash
docker compose -f docker-compose.production.yml up -d
```

Остановка:

```bash
docker compose -f docker-compose.production.yml down
```

---

## 🗄 Database Migrations

Создать миграцию:

```bash
alembic revision --autogenerate -m "migration_name"
```

Применить миграции:

```bash
alembic upgrade head
```

---

## 🧪 Testing

Запуск тестов:

```bash
pytest
```

Покрытие:

```bash
pytest --cov=app
```

Текущее покрытие проекта:

```text
73%
```

---

## 🔍 Code Quality

Форматирование:

```bash
black .
```

Сортировка импортов:

```bash
isort .
```

---

## 🔄 CI/CD

GitHub Actions автоматически выполняет:

* Проверку Black
* Проверку isort
* Запуск Pytest
* Проверку покрытия
* Сборку Docker-образа
* Публикацию образа в Docker Hub

Workflow запускается при:

* Push в `master`
* Pull Request в `master`

---

## 🐋 Docker Hub

Образ проекта:

```bash
docker pull pupsich460/workout-tracker-api:latest
```

---

## 📚 API Documentation

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

## 📌 Main Endpoints

| Method | Endpoint                | Description              |
| ------ | ----------------------- | ------------------------ |
| POST   | `/auth/register`        | User registration        |
| POST   | `/auth/jwt/login`       | JWT login                |
| GET    | `/exercises/`           | List exercises           |
| POST   | `/exercises/`           | Create exercise          |
| GET    | `/workouts/`            | List workouts            |
| POST   | `/workouts/`            | Create workout           |
| POST   | `/workouts/ai/generate` | Generate workout with AI |
| GET    | `/workout-logs/`        | List workout logs        |
| POST   | `/workout-logs/`        | Create workout log       |
| POST   | `/users/link-telegram`  | Link Telegram account    |

---
