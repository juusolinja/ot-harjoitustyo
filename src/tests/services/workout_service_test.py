import unittest
from tests.fake_repositories.fake_workout_repository import FakeWorkoutRepository
from services.workout_service import WorkoutService
from dto.movement_option import MovementOption

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

    def test_validate_set_with_correct_set(self):
        errors = self.workout_service.validate_set(self.default_set)

        self.assertEqual(errors, {})

    def test_validate_set_with_incorrect_set(self):
        incorrect_set = {
            "movement": None,
            "weight": -20,
            "reps": 0.5,
            "rir": -2
        }
        errors = self.workout_service.validate_set(incorrect_set)

        self.assertIn("movement", errors)
        self.assertIn("weight", errors)
        self.assertIn("reps", errors)
        self.assertIn("rir", errors)

    def test_validate_workout_with_incorrect_workout(self):
        workout_metadata = {
            "title": "test",
            "date": "2026-13-11",
            "notes": "",
            "duration": 60
        }
        errors = self.workout_service.validate_workout(workout_metadata, [])

        self.assertIn("date", errors)
        self.assertIn("general", errors)
