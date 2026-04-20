import unittest
from repositories.workout_repository import workout_repository
from repositories.movement_repository import movement_repository
from repositories.muscle_group_repository import muscle_group_repository
from entities.workout import Workout
from entities.set_entry import SetEntry
from entities.movement import Movement
from entities.muscle_group import MuscleGroup


class TestWorkoutRepository(unittest.TestCase):
    def setUp(self):
        workout_repository.delete_all()
        movement_repository.delete_all()
        muscle_group_repository.delete_all()

        muscle_group = MuscleGroup(
            name="Chest"
        )
        self._muscle_group = muscle_group_repository.create(
            muscle_group=muscle_group)
        movement = Movement(
            name="Bench Press", primary_muscle_group=muscle_group
        )
        self._movement = movement_repository.create(movement=movement)
        self._workout = Workout(
            title="Test workout",
            date="1999-12-31",
            notes="Test notes",
            duration=60,
            sets=[
                SetEntry(
                    movement=self._movement,
                    reps=10,
                    weight=100.0,
                    rir=1
                )
            ]
        )

    def test_create(self):
        created = workout_repository.create(self._workout)
        fetched = workout_repository.get_by_id(created.id)

        self.assertEqual(fetched.title, self._workout.title)
        self.assertEqual(fetched.date, self._workout.date)
        self.assertEqual(fetched.notes, self._workout.notes)
        self.assertEqual(fetched.duration, self._workout.duration)
        self.assertEqual(fetched.sets[0].movement.name, self._movement.name)
        self.assertEqual(fetched.sets[0].reps, self._workout.sets[0].reps)
        self.assertEqual(fetched.sets[0].weight, self._workout.sets[0].weight)
        self.assertEqual(fetched.sets[0].rir, self._workout.sets[0].rir)

    