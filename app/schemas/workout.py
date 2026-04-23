from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from app.schemas.workout_exercise import WorkoutExerciseDB


class FitnessLevel(str, Enum):
    beginner = "Новичок"
    intermediate = "Промежуточный"
    advanced = "Продвинутый"


class WorkoutBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")

class WorkoutGenerateRequest(BaseModel):
    goal: str
    current_weight: int
    days_per_week: int
    level: FitnessLevel


class WorkoutDB(WorkoutBase):
    id: int
    workout_exercises: list[WorkoutExerciseDB] = []

    model_config = ConfigDict(from_attributes=True)
