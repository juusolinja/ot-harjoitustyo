from entities.workout import Workout
from entities.set_entry import SetEntry

from repositories.workout_repository import (
    workout_repository as default_workout_repository
)

from repositories.movement_repository import (
    movement_repository as default_movement_repository
)


class WorkoutService:
    def __init__(
            self, workout_repository=default_workout_repository,
            movement_repository=default_movement_repository
        ):
        self._workout_repository = workout_repository
        self._movement_repository = movement_repository

    def create_workout(self, title, date, duration, notes, sets):
        set_entries = [
            SetEntry(
                movement=s["movement"],
                reps=s["reps"],
                weight=s["weight"],
                rir=s["rir"]
            )
            for s in sets
        ]
        workout = self._workout_repository.create(
            Workout(title=title, date=date, duration=duration,
                    notes=notes, sets=set_entries)
        )
        return workout

    def get_workout_by_id(self, workout_id):
        return self._workout_repository.get_by_id(workout_id)

    def get_all_workout_summaries(self):
        return self._workout_repository.get_all_workout_summaries()

    def get_all_movement_options(self):
        return self._movement_repository.get_all_movement_options()

    def validate_set(self):
        return []

    def validate_workout(self):
        return []

    def update_workout(self, workout, pending_metadata, pending_sets):
        set_entires = [
            SetEntry(
                movement=s["movement"],
                reps=s["reps"],
                weight=s["weight"],
                rir=s["rir"]
            )
            for s in pending_sets
        ]
        updated_workout = Workout(
            workout_id=workout.id,
            title=pending_metadata["title"],
            date=pending_metadata["date"],
            notes=pending_metadata["notes"],
            duration=pending_metadata["duration"],
            sets=set_entires
        )
        return self._workout_repository.update(updated_workout)

    def delete_workout(self, workout):
        self._workout_repository.delete(workout)


workout_service = WorkoutService()
