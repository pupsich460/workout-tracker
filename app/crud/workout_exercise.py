from app.crud.base import CRUDBase
from app.models.workout_exercise import WorkoutExercise


class CRUDWorkoutExercise(CRUDBase):
    pass


workout_exercise_crud = CRUDWorkoutExercise(WorkoutExercise)
