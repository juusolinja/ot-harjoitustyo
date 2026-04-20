import unittest
from services.workout_service import WorkoutService
from dto.workout_summary import WorkoutSummary
from dto.movement_option import MovementOption

class FakeWorkoutRepository:
    def __init__(self, workouts=None):
        self.workouts = workouts or []
        self._next_id = 1

    def delete_all(self):
        self.workouts = []
        self._next_id = 1

    def get_all_workout_summaries(self):
        return sorted(
            [
                WorkoutSummary(
                    workout_id=w.id,
                    date=w.date,
                    title=w.title,
                    duration=w.duration
                )
                for w in self.workouts
            ],
            key=lambda w: (w.date, w.workout_id),
            reverse=True
        )

    def get_by_id(self, workout_id):
        return next(
            (w for w in self.workouts if w.id == workout_id),
            None
        )

    def create(self, workout):
        workout.id = self._next_id
        self._next_id += 1
        self.workouts.append(workout)
        return workout

    def update(self, workout):
        for i, w in enumerate(self.workouts):
            if w.id == workout.id:
                self.workouts[i] = workout
                return workout
        return workout

    def delete(self, workout):
        self.workouts = [w for w in self.workouts if w.id != workout.id]

class TestWorkoutService(unittest.TestCase):
    def setUp(self):
        self.workout_service = WorkoutService(FakeWorkoutRepository())

        self.default_set = {
            "movement": MovementOption(1, "Bench Press"),
            "weight": "100",
            "reps": "10",
            "rir": 1
        }
    
    def test_create_workout(self):
        self.workout_service.create_workout(
            "Test title",
            "1999-12-31",
            60,
            "Test notes",
            [self.default_set]
        )

        workout_summaries = self.workout_service.get_all_workout_summaries()

        self.assertEqual(workout_summaries[0].title, "Test title")
        self.assertEqual(len(workout_summaries), 1)

    def test_validate_set(self):
        errors = self.workout_service.validate_set(self.default_set)

        self.assertEqual(errors, {})