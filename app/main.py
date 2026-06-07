from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.exceptions import global_exception_handler
from app.core.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    logger.info("Приложение запущено")
    yield
    logger.info("Приложение остановлено")


app = FastAPI(title=settings.app_title, lifespan=lifespan)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(main_router)
