from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from app.api.validators import (check_exercise_duplicate_in_workout,
                                validate_exercise_owner,
                                validate_workout_exercise,
                                validate_workout_owner)
from app.core.dependencies import RedisDep, SessionDep
from app.core.user import current_user
from app.crud.workout import workout_crud
from app.crud.workout_exercise import workout_exercise_crud
from app.models import User
from app.schemas.workout import (WorkoutCreate, WorkoutDB,
                                 WorkoutGenerateRequest, WorkoutUpdate)
from app.schemas.workout_exercise import (WorkoutExerciseCreate,
                                          WorkoutExerciseDB)
from app.services.ai_workout import create_workout_from_ai, generate_workout
from app.tasks.reminders import send_workout_reminder

router = APIRouter()


@router.get(
    "/",
    response_model=list[WorkoutDB],
    response_model_exclude_none=True,
    summary="Показать список всех тренировок",
)
async def get_workouts(
    session: SessionDep,
    user: User = Depends(current_user),
    limit: int = 10,
    offset: int = 0,
):
    """Показать список всех тренировок."""
    workouts = await workout_crud.get_multi_by_user(
        session, user.id, limit=limit, offset=offset
    )

    return workouts


@router.get("/redis-test")
async def redis_test(redis: RedisDep):
    await redis.set("test", "hello")
    return {"value": await redis.get("test")}


@router.get(
    "/{workout_id}",
    response_model=WorkoutDB,
    response_model_exclude_none=True,
    summary="Показать тренировку по id",
)
async def get_workout_by_id(
    workout_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Показать тренировку по id."""
    return await validate_workout_owner(workout_id, user, session)


@router.get(
    "/{workout_id}/exercises",
    response_model=list[WorkoutExerciseDB],
    response_model_exclude_none=True,
    summary="Показать упражнения в тренировке по id",
)
async def get_workout_exercises(
    workout_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Показать упражнения в тренировке по id."""
    workout = await validate_workout_owner(workout_id, user, session)
    return workout.workout_exercises


@router.post(
    "/ai/generate",
    response_model=WorkoutDB,
    response_model_exclude_none=True,
    summary="Сгенерировать тренировку на основе цели, текущего веса, количества тренировок в неделю и уровня фитнеса",
)
async def generate_workout_endpoint(
    obj_in: WorkoutGenerateRequest,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Сгенерировать тренировку на основе цели, текущего веса, количества тренировок в неделю и уровня фитнеса."""
    workout_data = await generate_workout(
        obj_in.goal, obj_in.current_weight, obj_in.days_per_week, obj_in.level
    )
    return await create_workout_from_ai(workout_data, session, user)


@router.post(
    "/",
    response_model=WorkoutDB,
    response_model_exclude_none=True,
    summary="Создать тренировку",
)
async def create_workout_endpoint(
    obj_in: WorkoutCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Создать тренировку."""
    workout = await workout_crud.create(obj_in, session, user)

    if obj_in.remind_in_minutes is not None:
        if not user.telegram_id:
            raise HTTPException(
                status_code=400,
                detail="Telegram не привязан. Невозможно создать напоминание.",
            )

    if obj_in.remind_in_minutes is not None:
        send_workout_reminder.apply_async(
            args=[user.telegram_id, f"Напоминание о тренировке: {workout.name}"],
            countdown=obj_in.remind_in_minutes * 60,
        )
    return workout


@router.post(
    "/{workout_id}/exercises",
    response_model=WorkoutExerciseDB,
    response_model_exclude_none=True,
    summary="Добавить упражнение в тренировку по id тренировки",
    status_code=HTTPStatus.CREATED,
)
async def add_exercise_to_workout(
    workout_id: int,
    obj: WorkoutExerciseCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Добавить упражнение в тренировку по id тренировки."""
    await validate_workout_owner(workout_id, user, session)

    await validate_exercise_owner(obj.exercise_id, user, session)

    await check_exercise_duplicate_in_workout(
        workout_id=workout_id, exercise_id=obj.exercise_id, session=session
    )

    obj_in = obj.model_copy(update={"workout_id": workout_id})
    return await workout_exercise_crud.create(obj_in, session)


@router.delete(
    "/{workout_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удалить тренировку по id",
)
async def delete_workout_by_id(
    workout_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Удалить тренировку по id."""
    workout = await validate_workout_owner(workout_id, user, session)
    await workout_crud.remove(workout, session)


@router.patch(
    "/{workout_id}",
    response_model=WorkoutDB,
    response_model_exclude_none=True,
    summary="Обновить тренировку по id",
)
async def update_workout_by_id(
    workout_id: int,
    obj_in: WorkoutUpdate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Обновить тренировку по id."""
    workout = await validate_workout_owner(workout_id, user, session)

    return await workout_crud.update(workout, obj_in, session)


@router.delete(
    "/{workout_id}/exercises/{exercise_id}",
    status_code=HTTPStatus.NO_CONTENT,
    summary="Удалить упражнение из тренировки по id тренировки и id упражнения",
)
async def delete_exercise_from_workout(
    workout_id: int,
    exercise_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Удалить упражнение из тренировки по id тренировки и id упражнения."""
    await validate_workout_owner(workout_id, user, session)
    workout_exercise = await validate_workout_exercise(workout_id, exercise_id, session)
    await workout_exercise_crud.remove(workout_exercise, session)
