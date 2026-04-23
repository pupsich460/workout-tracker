from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.exercise import Exercise


class CRUDExercise(CRUDBase):
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

    async def get_exercise_id_by_name(
        self,
        exercise_name: str,
        session,
        user,
    ) -> int | None:
        db_project_id = await session.execute(
            select(Exercise.id).where(
                Exercise.name == exercise_name, Exercise.user_id == user.id
            )
        )
        return db_project_id.scalars().first()

    async def get_exercises_by_user(
        self,
        session,
        user,
    ) -> list[Exercise]:
        result = await session.execute(
            select(self.model).where(self.model.user_id == user.id)
        )
        return result.scalars().all()

    async def get_exercise_by_id(
        self,
        exercise_id: int,
        session,
        user,
    ) -> Exercise | None:
        result = await session.execute(
            select(self.model).where(
                self.model.id == exercise_id, self.model.user_id == user.id
            )
        )
        return result.scalars().first()


exercise_crud = CRUDExercise(Exercise)
