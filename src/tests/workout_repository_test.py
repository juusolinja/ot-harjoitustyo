import unittest
from repositories.workout_repository import workout_repository
from entities.workout import Workout

class TestWorkoutRepository(unittest.TestCase):
    def setUp(self):
        workout_repository.delete_all()

        self.workout_a = Workout("2026-01-01", "test workout a")
        self.workout_b = Workout("2026-01-02", "testing wokout b")

    def test_get_all(self):
        workout_repository.create(self.workout_a)
        workout_repository.create(self.workout_b)
        workouts = workout_repository.get_all()

        self.assertEqual(len(workouts), 2)
        self.assertEqual((workouts[0].date, workouts[0].notes), (self.workout_a.date, self.workout_a.notes))
        self.assertEqual((workouts[1].date, workouts[1].notes), (self.workout_b.date, self.workout_b.notes))
