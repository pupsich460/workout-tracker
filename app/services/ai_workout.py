import json

import httpx

from app.core.config import settings


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

    data = response.json()
    print(data)
    text = data["choices"][0]["message"]["content"]
    result = json.loads(text)

    # если вернула список — берём первый элемент
    if isinstance(result, list):
        result = result[0]

    return result
