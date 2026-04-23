from app.core.db import Base, CommonMixin


class BaseModel(Base, CommonMixin):
    __abstract__ = True
