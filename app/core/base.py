"""Импорты класса Base и всех моделей для Alembic."""

from app.core.db import Base  # noqa
from app.models.exercise import Exercise  # noqa
from app.models.user import User  # noqa
from app.models.workout import Workout  # noqa
from app.models.workout_exercise import WorkoutExercise  # noqa
from app.models.workout_log import WorkoutLog  # noqa
from app.models.workout_schedule import WorkoutSchedule  # noqa
