from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class WorkoutLog(BaseModel):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    workout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workout.id"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    status: Mapped[bool] = mapped_column(nullable=False)
