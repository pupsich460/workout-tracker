from aiogram.fsm.state import State, StatesGroup


class AuthStates(StatesGroup):
    waiting_email = State()
    waiting_password = State()


class GenerateStates(StatesGroup):
    waiting_goal = State()
    waiting_weight = State()
    waiting_days = State()
    waiting_level = State()


class LogStates(StatesGroup):
    waiting_workout_id = State()
    waiting_notes = State()


class CreateWorkoutStates(StatesGroup):
    waiting_name = State()
    waiting_description = State()


class AddExerciseStates(StatesGroup):
    waiting_exercise_name = State()
    waiting_sets = State()
    waiting_reps = State()


class ScheduleStates(StatesGroup):
    waiting_workout = State()
    waiting_weekday = State()
    waiting_time = State()
    waiting_reminder_minutes = State()
