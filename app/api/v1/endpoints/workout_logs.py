from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.v1.validators import (
    check_workout_log_duplicate,
    validate_workout_log_owner,
    validate_workout_owner,
)
from app.core.dependencies import SessionDep
from app.core.user import current_user
from app.crud.workout_log import workout_log_crud
from app.models import User
from app.schemas.workout_log import WorkoutLogCreate, WorkoutLogDB, WorkoutLogUpdate

router = APIRouter()


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
    workouts_log = await workout_log_crud.get_multi_by_user(session, user.id)

    return workouts_log


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
    workout_log = await validate_workout_log_owner(workout_log_id, user, session)
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
    await validate_workout_owner(workout_log.workout_id, user, session)
    await check_workout_log_duplicate(
        workout_id=workout_log.workout_id,
        user=user,
        date=workout_log.date,
        session=session,
    )
    return await workout_log_crud.create(workout_log, session, user)


@router.patch(
    "/{workout_log_id}",
    response_model=WorkoutLogDB,
    response_model_exclude_none=True,
    summary="Обновить лог тренировки по id",
)
async def update_workout_log(
    workout_log_id: int,
    obj_in: WorkoutLogUpdate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Обновить лог тренировки по id."""
    workout_log = await validate_workout_log_owner(workout_log_id, user, session)
    return await workout_log_crud.update(workout_log, obj_in, session)


@router.delete(
    "/{workout_log_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удалить лог тренировки по id",
)
async def delete_workout_log_by_id(
    workout_log_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    workout_log = await validate_workout_log_owner(workout_log_id, user, session)
    await workout_log_crud.remove(workout_log, session)
