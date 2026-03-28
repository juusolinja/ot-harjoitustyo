from entities.workout import Workout

from repositories.workout_repository import (
    workout_repository as default_workout_repository
)

class WorkoutService:
    def __init__(self, workout_repository=default_workout_repository):
        self._workout_repository = workout_repository

    def create_workout(self, date, notes):
        workout = Workout(date=date, notes=notes)

        return self._workout_repository.create(workout)
    
    def get_all_workouts(self):
        return self._workout_repository.get_all()
    
workout_service = WorkoutService()
    