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

    async def get_by_user(
        self,
        user_id: int,
        session,
    ) -> list[WorkoutLog]:
        result = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_id(
        self,
        workout_log_id: int,
        session,
        user,
    ) -> WorkoutLog | None:
        result = await session.execute(
            select(self.model).where(
                self.model.id == workout_log_id, self.model.user_id == user.id
            )
        )
        return result.scalars().first()


workout_log_crud = CRUDWorkoutLog(WorkoutLog)
