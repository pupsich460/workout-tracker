from pydantic import BaseModel, ConfigDict, Field


class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")


class ExerciseDB(ExerciseBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
