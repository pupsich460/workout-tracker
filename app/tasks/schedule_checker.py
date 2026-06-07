import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.celery_app import celery_app
from app.core.db import AsyncSessionLocal
from app.models.workout_schedule import WorkoutSchedule
from app.tasks.reminders import send_workout_reminder


async def _check_workout_schedules():
    now = datetime.now(timezone.utc)
    current_weekday = now.weekday()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(WorkoutSchedule)
            .options(
                selectinload(WorkoutSchedule.workout),
                selectinload(WorkoutSchedule.user),
            )
            .where(
                WorkoutSchedule.is_active.is_(True),
                WorkoutSchedule.weekday == current_weekday,
            )
        )

        schedules = result.scalars().all()

        for schedule in schedules:
            workout_datetime = datetime.combine(
                now.date(),
                schedule.workout_time,
                tzinfo=timezone.utc,
            )

            reminder_datetime = workout_datetime - timedelta(
                minutes=schedule.reminder_minutes_before
            )

            already_reminded_today = (
                schedule.last_reminder_at is not None
                and schedule.last_reminder_at.date() == now.date()
            )

            if already_reminded_today:
                continue

            if reminder_datetime <= now < workout_datetime:
                if schedule.user.telegram_id:
                    send_workout_reminder.delay(
                        schedule.user.telegram_id,
                        f"Напоминание: тренировка «{schedule.workout.name}» скоро начнётся!",
                    )

                    schedule.last_reminder_at = now

        await session.commit()


@celery_app.task
def check_workout_schedules():
    asyncio.run(_check_workout_schedules())
