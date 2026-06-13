from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import SessionDep
from app.core.user import current_user
from app.crud.workout_schedule import workout_schedule_crud
from app.models.user import User
from app.schemas.workout_schedule import WorkoutScheduleCreate, WorkoutScheduleDB

router = APIRouter()


@router.post(
    "/schedules/",
    response_model=WorkoutScheduleDB,
    summary="Создать расписание тренировки",
)
async def create_workout_schedule(
    obj_in: WorkoutScheduleCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    try:
        return await workout_schedule_crud.create(obj_in, session, user)
    except ValueError:
        raise HTTPException(status_code=404, detail="Workout not found")


@router.get(
    "/schedules/",
    response_model=list[WorkoutScheduleDB],
    summary="Получить расписания тренировок",
)
async def get_my_workout_schedules(
    session: SessionDep,
    user: User = Depends(current_user),
):
    return await workout_schedule_crud.get_user_schedules(session, user)


@router.patch(
    "/schedules/{schedule_id}/deactivate",
    summary="Деактивировать расписание тренировки",
)
async def deactivate_workout_schedule(
    schedule_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    try:
        await workout_schedule_crud.deactivate(schedule_id, session, user)
    except ValueError:
        raise HTTPException(status_code=404, detail="Schedule not found")


@router.delete(
    "/schedules/{schedule_id}",
    summary="Удалить расписание тренировки",
)
async def delete_workout_schedule(
    schedule_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    try:
        await workout_schedule_crud.delete(schedule_id, session, user)
    except ValueError:
        raise HTTPException(status_code=404, detail="Schedule not found")
