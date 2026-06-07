from datetime import time

from pydantic import BaseModel, Field


class WorkoutScheduleCreate(BaseModel):
    workout_id: int
    weekday: int = Field(ge=0, le=6)  # 0 - понедельник, 6 - воскресенье
    workout_time: time
    reminder_minutes_before: int = Field(default=60, gt=0, le=1440)


class WorkoutScheduleDB(WorkoutScheduleCreate):
    id: int
    user_id: int
    is_active: bool

    class Config:
        from_attributes = True
