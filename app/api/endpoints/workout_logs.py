from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.workout_log import workout_log_crud
from app.models import User
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogDB

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/",
    response_model=list[WorkoutLogDB],
    response_model_exclude_none=True,
    summary="Показать список всех логов тренировок",
)
async def get_workout_logs(
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Показать список всех логов тренировок."""
    return await workout_log_crud.get_multi_by_user(session, user.id)


@router.get(
    "/{workout_log_id}",
    response_model=WorkoutLogDB,
    response_model_exclude_none=True,
    summary="Показать лог тренировки по id",
)
async def get_workout_log_by_id(
    workout_log_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Показать лог тренировки по id."""
    workout_log = await workout_log_crud.get_by_id(workout_log_id, session, user)
    if not workout_log:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Лог тренировки не найден"
        )
    return workout_log


@router.post(
    "/",
    response_model=WorkoutLogDB,
    response_model_exclude_none=True,
    summary="Отметить тренировку как выполненную",
    status_code=HTTPStatus.CREATED,
)
async def create_workout_log(
    workout_log: WorkoutLogCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Отметить тренировку как выполненную."""
    return await workout_log_crud.create(workout_log, session, user)
