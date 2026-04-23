from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.exercise import exercise_crud
from app.crud.workout import workout_crud
from app.models import User


async def validate_workout_owner(
    workout_id: int,
    user: User,
    session: AsyncSession,
):
    """Проверить, что тренировка существует и принадлежит пользователю."""
    workout = await workout_crud.get(workout_id, session)
    if not workout or workout.user_id != user.id:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Тренировка не найдена")
    return workout


async def check_name_duplicate(
    exercise_name: str, session: AsyncSession, user: User
) -> None:
    exercise_id = await exercise_crud.get_exercise_id_by_name(
        exercise_name, session, user
    )
    if exercise_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Упражнение с таким именем уже существует!",
        )
