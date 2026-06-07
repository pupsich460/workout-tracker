from enum import Enum

from pydantic import (BaseModel, ConfigDict, Field, field_validator,
                      model_validator)

from app.schemas.workout_exercise import WorkoutExerciseDB


def clean_string(v: str, min_len: int = 1) -> str:
    v = v.strip()
    if len(v) < min_len:
        raise ValueError("Строка слишком короткая")
    return v


def clean_optional_string(v: str | None) -> str | None:
    if v is None:
        return v
    v = v.strip()
    return v or None


class FitnessLevel(str, Enum):
    beginner = "Новичок"
    intermediate = "Промежуточный"
    advanced = "Продвинутый"


class WorkoutBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        return clean_string(v, min_len=2)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None):
        return clean_optional_string(v)


class WorkoutCreate(WorkoutBase):
    remind_in_minutes: int | None = Field(None, gt=0, le=10080)


class WorkoutUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None):
        if v is None:
            return v
        return clean_string(v, min_len=2)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None):
        return clean_optional_string(v)

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.name is None and self.description is None:
            raise ValueError("Хотя бы одно поле должно быть передано")
        return self


class WorkoutGenerateRequest(BaseModel):
    goal: str = Field(..., min_length=3, max_length=100)
    current_weight: int = Field(..., gt=0, le=500)
    days_per_week: int = Field(..., gt=0, le=7)
    level: FitnessLevel

    model_config = ConfigDict(extra="forbid")

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str):
        return clean_string(v, min_len=3)


class WorkoutDB(WorkoutBase):
    id: int
    workout_exercises: list[WorkoutExerciseDB] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, extra="forbid")
