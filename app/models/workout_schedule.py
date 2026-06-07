from datetime import datetime, time

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class WorkoutSchedule(BaseModel):
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workout.id"),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
    )

    weekday: Mapped[int] = mapped_column(Integer, nullable=False)
    workout_time: Mapped[time] = mapped_column(Time, nullable=False)

    reminder_minutes_before: Mapped[int] = mapped_column(
        Integer,
        default=60,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    last_reminder_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    workout = relationship("Workout", back_populates="schedules")

    user = relationship("User")
