from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.workout import Workout
from app.models.workout_schedule import WorkoutSchedule
from app.schemas.workout_schedule import WorkoutScheduleCreate


class CRUDWorkoutSchedule(CRUDBase):
    async def create(
        self,
        obj_in: WorkoutScheduleCreate,
        session: AsyncSession,
        user,
    ) -> WorkoutSchedule:
        workout = await session.get(Workout, obj_in.workout_id)

        if workout is None or workout.user_id != user.id:
            raise ValueError("Workout not found")

        db_obj = WorkoutSchedule(
            **obj_in.model_dump(),
            user_id=user.id,
        )

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    async def get_user_schedules(
        self,
        session: AsyncSession,
        user,
    ) -> list[WorkoutSchedule]:
        result = await session.execute(
            select(WorkoutSchedule).where(
                WorkoutSchedule.user_id == user.id,
                WorkoutSchedule.is_active.is_(True),
            )
        )
        return list(result.scalars().all())

    async def deactivate(
        self,
        schedule_id: int,
        session: AsyncSession,
        user,
    ) -> None:
        schedule = await session.get(WorkoutSchedule, schedule_id)

        if schedule is None or schedule.user_id != user.id:
            raise ValueError("Schedule not found")

        schedule.is_active = False
        session.add(schedule)
        await session.commit()
        await session.refresh(schedule)

        return schedule

    async def delete(
        self,
        schedule_id: int,
        session: AsyncSession,
        user,
    ) -> None:
        schedule = await session.get(WorkoutSchedule, schedule_id)

        if schedule is None or schedule.user_id != user.id:
            raise ValueError("Schedule not found")

        await session.delete(schedule)
        await session.commit()


workout_schedule_crud = CRUDWorkoutSchedule(WorkoutSchedule)
