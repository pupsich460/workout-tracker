from pydantic import BaseModel, ConfigDict, Field

from app.schemas.exercise import ExerciseDB


class WorkoutExerciseBase(BaseModel):
    sets: int = Field(..., gt=0)
    reps: int = Field(..., gt=0)
    order: int | None = Field(None, gt=0)

    model_config = ConfigDict(extra="forbid")


class WorkoutExerciseCreate(WorkoutExerciseBase):
    workout_id: int = Field(..., gt=0)
    exercise_id: int = Field(..., gt=0)


class WorkoutExerciseUpdate(BaseModel):
    workout_id: int | None = Field(None, gt=0)
    exercise_id: int | None = Field(None, gt=0)
    sets: int | None = Field(None, gt=0)
    reps: int | None = Field(None, gt=0)
    order: int | None = Field(None, gt=0)

    model_config = ConfigDict(extra="forbid")


class WorkoutExerciseDB(WorkoutExerciseBase):
    id: int
    exercise: ExerciseDB

    model_config = ConfigDict(from_attributes=True)
