from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def normalize_datetime(v: datetime) -> datetime:
    if v.tzinfo is None:
        v = v.replace(tzinfo=timezone.utc)
    return v.astimezone(timezone.utc)


class WorkoutLogBase(BaseModel):
    workout_id: int = Field(..., gt=0)

    model_config = ConfigDict(extra="forbid")


class WorkoutLogCreate(WorkoutLogBase):
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("date")
    @classmethod
    def date_not_in_future(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v > datetime.now(timezone.utc):
            raise ValueError("Дата не может быть в будущем")
        return v


class WorkoutLogUpdate(BaseModel):
    status: bool | None = None

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def at_least_one_field(self):
        if self.status is None:
            raise ValueError("Хотя бы одно поле должно быть передано")
        return self


class WorkoutLogDB(WorkoutLogBase):
    id: int
    user_id: int
    date: datetime
    status: bool = Field(...)

    model_config = ConfigDict(from_attributes=True, extra="forbid")
