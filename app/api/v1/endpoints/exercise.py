from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.v1.validators import check_name_duplicate, validate_exercise_owner
from app.core.dependencies import SessionDep
from app.core.user import current_user
from app.crud.exercise import exercise_crud
from app.models import User
from app.schemas.exercise import ExerciseCreate, ExerciseDB, ExerciseUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=list[ExerciseDB],
    response_model_exclude_none=True,
    summary="Показать список всех упражнений",
)
async def get_exercises(
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Показать список всех упражнений."""
    exercises = await exercise_crud.get_multi_by_user(session, user.id)
    return exercises


@router.get(
    "/{exercise_id}",
    response_model=ExerciseDB,
    response_model_exclude_none=True,
    summary="Показать упражнение по id",
)
async def get_exercise_by_id(
    exercise_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Показать упражнение по id."""
    exercise = await validate_exercise_owner(exercise_id, user, session)
    return exercise


@router.delete(
    "/{exercise_id}",
    summary="Удалить упражнение по id",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_exercise_by_id(
    exercise_id: int,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Удалить упражнение по id."""
    exercise = await validate_exercise_owner(exercise_id, user, session)
    await exercise_crud.remove(exercise, session)


@router.post(
    "/",
    response_model=ExerciseDB,
    response_model_exclude_none=True,
    summary="Создать упражнение",
    status_code=HTTPStatus.CREATED,
)
async def create_exercise(
    exercise: ExerciseCreate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Создать упражнение."""
    await check_name_duplicate(exercise.name, session, user)
    return await exercise_crud.create(exercise, session, user)


@router.patch(
    "/{exercise_id}",
    response_model=ExerciseDB,
    response_model_exclude_none=True,
    summary="Обновить упражнение по id",
)
async def update_exercise_by_id(
    exercise_id: int,
    exercise: ExerciseUpdate,
    session: SessionDep,
    user: User = Depends(current_user),
):
    """Обновить упражнение по id."""
    db_exercise = await validate_exercise_owner(exercise_id, user, session)
    if exercise.name is not None:
        await check_name_duplicate(exercise.name, session, user)
    return await exercise_crud.update(db_exercise, exercise, session)
