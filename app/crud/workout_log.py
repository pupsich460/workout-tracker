from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.workout_log import WorkoutLog


class CRUDWorkoutLog(CRUDBase):
    async def create(
        self,
        obj_in,
        session,
        user,
    ):
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, user_id=user.id)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_by_fields(
        self,
        session,
        **filters,
    ):
        query = select(self.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().first()


workout_log_crud = CRUDWorkoutLog(WorkoutLog)
