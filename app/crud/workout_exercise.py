from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.workout_exercise import WorkoutExercise


class CRUDWorkoutExercise(CRUDBase):
    async def get_by_workout_and_exercise(
        self,
        workout_id: int,
        exercise_id: int,
        session,
    ) -> WorkoutExercise | None:
        result = await session.execute(
            select(self.model).where(
                self.model.workout_id == workout_id,
                self.model.exercise_id == exercise_id,
            )
        )
        return result.scalars().first()

    async def get_by_fields(
        self,
        session,
        **filters,
    ):
        query = select(self.model).filter_by(**filters)
        result = await session.execute(query)
        return result.scalars().first()


workout_exercise_crud = CRUDWorkoutExercise(WorkoutExercise)
