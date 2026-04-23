from app.crud.base import CRUDBase
from app.models.workout import Workout


class CRUDWorkout(CRUDBase):
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


workout_crud = CRUDWorkout(Workout)
