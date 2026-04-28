from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkoutLogBase(BaseModel):
    workout_id: int = Field(..., gt=0)

    model_config = ConfigDict(extra="forbid")


class WorkoutLogCreate(WorkoutLogBase):
    pass


class WorkoutLogUpdate(BaseModel):
    status: bool | None = None

    model_config = ConfigDict(extra="forbid")


class WorkoutLogDB(WorkoutLogBase):
    id: int
    user_id: int
    date: datetime
    status: bool = Field(...)

    model_config = ConfigDict(from_attributes=True)
