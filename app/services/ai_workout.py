import json
from http import HTTPStatus

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.crud.exercise import exercise_crud
from app.crud.workout import workout_crud
from app.crud.workout_exercise import workout_exercise_crud
from app.models.workout import Workout
from app.schemas.exercise import ExerciseCreate
from app.schemas.workout import WorkoutCreate
from app.schemas.workout_exercise import WorkoutExerciseCreate


async def generate_workout(
    goal: str, current_weight: int, days_per_week: int, level: str
) -> dict:
    prompt = f"""Ты персональный тренер. Составь план тренировки.

    Данные пользователя:
    - Цель: {goal}
    - Текущий вес: {current_weight} кг
    - Тренировок в неделю: {days_per_week}
    - Уровень: {level}

    Верни ТОЛЬКО один JSON объект, не массив. Строго такой формат:
    {{"name": "название тренировки", "exercises": [{{"name": "название упражнения", "sets": 3, "reps": 10}}]}}

    Никакого текста до или после JSON. Только JSON объект."""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()

        data = response.json()
        text = data["choices"][0]["message"]["content"]
        result = json.loads(text)

    except httpx.HTTPStatusError:
        raise HTTPException(HTTPStatus.BAD_GATEWAY, "Ошибка при запросе к AI сервису")
    except (json.JSONDecodeError, KeyError):
        raise HTTPException(HTTPStatus.BAD_GATEWAY, "Некорректный ответ от AI сервиса")

    if isinstance(result, list):
        result = result[0]

    return result


async def create_workout_from_ai(
    workout_data: dict,
    session,
    user,
) -> Workout:
    async with session.begin():
        workout_create = WorkoutCreate(name=workout_data["name"])
        workout = await workout_crud.create(workout_create, session, user)

        for exercise in workout_data["exercises"]:
            exercise_obj = await exercise_crud.create(
                ExerciseCreate(name=exercise["name"]), session, user
            )
            await workout_exercise_crud.create(
                WorkoutExerciseCreate(
                    workout_id=workout.id,
                    exercise_id=exercise_obj.id,
                    sets=exercise["sets"],
                    reps=exercise["reps"],
                ),
                session,
            )

    return workout
