from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.exercise import ExerciseDB


class WorkoutExerciseBase(BaseModel):
    sets: int = Field(..., gt=0, le=100)
    reps: int = Field(..., gt=0, le=1000)
    order: int | None = Field(None, gt=0)

    model_config = ConfigDict(extra="forbid")


class WorkoutExerciseCreate(WorkoutExerciseBase):
    workout_id: int = Field(..., gt=0)
    exercise_id: int = Field(..., gt=0)


class WorkoutExerciseUpdate(BaseModel):
    sets: int | None = Field(None, gt=0, le=100)
    reps: int | None = Field(None, gt=0, le=1000)
    order: int | None = Field(None, gt=0)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.sets is None and self.reps is None and self.order is None:
            raise ValueError("Хотя бы одно поле должно быть передано")
        return self


class WorkoutExerciseDB(WorkoutExerciseBase):
    id: int
    exercise: ExerciseDB

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
