from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.exceptions import global_exception_handler
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title=settings.app_title)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(main_router)
