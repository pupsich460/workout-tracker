from fastapi_users import schemas
from pydantic import BaseModel, Field


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class TelegramLinkRequest(BaseModel):
    telegram_id: int = Field(..., gt=0)


class TelegramLinkByCodeRequest(BaseModel):
    telegram_id: int
    code: str
