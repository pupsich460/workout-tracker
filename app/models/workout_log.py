from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class WorkoutLog(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, index=True
    )
    workout_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workout.id"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    status: Mapped[bool] = mapped_column(nullable=False, default=False)
