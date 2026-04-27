import unittest
from services.analysis_service import AnalysisService
from tests.fake_repositories.fake_workout_repository import FakeWorkoutRepository
from tests.fake_repositories.fake_muscle_group_repository import FakeMuscleGroupRepository
from entities.muscle_group import MuscleGroup
from entities.workout import Workout
from entities.movement import Movement
from entities.set_entry import SetEntry
from date_utils import get_current_week_range

class TestAnalysisService(unittest.TestCase):
    def setUp(self):
        monday, sunday = get_current_week_range()
        self._default_muscle_group = MuscleGroup("Chest", 0)
        self._default_movement = Movement("Bench Press", self._default_muscle_group, 0)
        self._workout_a = Workout(
            "Monday",
            monday,
            "",
            100,
            60,
            [SetEntry(self._default_movement, 10, 100, 1)]
        )
        self._workout_b = Workout(
            "Sunday",
            sunday,
            "",
            101,
            60,
            [SetEntry(self._default_movement, 10, 100, 1)]
        )
        self._workout_repo = FakeWorkoutRepository([self._workout_a, self._workout_b])
        self._muscle_group_repo = FakeMuscleGroupRepository([self._default_muscle_group])
        self.analysis_service = AnalysisService(self._workout_repo, self._muscle_group_repo)

    def test_get_current_week_volumes(self):
        volumes = self.analysis_service.get_current_week_volumes()
        self.assertEqual(volumes["Chest"], 2)
