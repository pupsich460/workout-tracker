from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.exercise import exercise_crud
from app.crud.workout import workout_crud
from app.crud.workout_exercise import workout_exercise_crud
from app.crud.workout_log import workout_log_crud
from app.models import User


async def _validate_owner(obj, user):
    """Проверить, что объект существует и принадлежит пользователю."""
    if not obj or obj.user_id != user.id:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Объект не найден")
    return obj


async def validate_workout_owner(
    workout_id: int,
    user: User,
    session: AsyncSession,
):
    """Проверить, что тренировка существует и принадлежит пользователю."""
    workout = await workout_crud.get(workout_id, session)
    return await _validate_owner(workout, user)


async def validate_exercise_owner(
    exercise_id: int,
    user: User,
    session: AsyncSession,
):
    """Проверить, что упражнение существует и принадлежит пользователю."""
    exercise = await exercise_crud.get(exercise_id, session)
    return await _validate_owner(exercise, user)


async def validate_workout_log_owner(
    workout_log_id: int,
    user: User,
    session: AsyncSession,
):
    """Проверить, что лог тренировки существует и принадлежит пользователю."""
    workout_log = await workout_log_crud.get(workout_log_id, session)
    return await _validate_owner(workout_log, user)


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


async def validate_workout_exercise(
    workout_id: int,
    exercise_id: int,
    session: AsyncSession,
):
    workout_exercise = await workout_exercise_crud.get_by_workout_and_exercise(
        workout_id, exercise_id, session
    )
    if not workout_exercise:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Упражнение в тренировке не найдено")
    return workout_exercise


async def check_workout_log_duplicate(
    workout_id: int, session: AsyncSession, user: User, date: datetime.date
) -> None:
    existing = await workout_log_crud.get_by_fields(
        session, workout_id=workout_id, user_id=user.id, date=date
    )

    if existing:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Лог тренировки с таким workout_id уже существует!",
        )


async def check_exercise_duplicate_in_workout(
    workout_id: int,
    exercise_id: int,
    session: AsyncSession,
) -> None:
    existing = await workout_exercise_crud.get_by_fields(
        session, workout_id=workout_id, exercise_id=exercise_id
    )
    if existing:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Упражнение уже добавлено в тренировку!",
        )


async def check_telegram_id_duplicate(
    telegram_id: int,
    session: AsyncSession,
) -> None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Этот Telegram аккаунт уже привязан к другому пользователю",
        )
