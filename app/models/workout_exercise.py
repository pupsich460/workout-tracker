from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class WorkoutExercise(BaseModel):
    workout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workout.id"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("exercise.id"), nullable=False
    )
    sets: Mapped[int] = mapped_column(Integer, nullable=False)
    reps: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    workout = relationship(
        "Workout", back_populates="workout_exercises", lazy="selectin"
    )
    exercise = relationship(
        "Exercise", back_populates="workout_exercises", lazy="selectin"
    )
