from fastapi import APIRouter

from app.api.endpoints import (
    exercise_router,
    user_router,
    workout_log_router,
    workout_router,
    workout_schedule_router,
)

main_router = APIRouter()

main_router.include_router(exercise_router, prefix="/exercises", tags=["exercises"])
main_router.include_router(workout_router, prefix="/workouts", tags=["workouts"])
main_router.include_router(
    workout_log_router, prefix="/workout-logs", tags=["workout-logs"]
)
main_router.include_router(
    workout_schedule_router,
    prefix="/workout-schedules",
    tags=["Workout schedules"],
)
main_router.include_router(user_router)
