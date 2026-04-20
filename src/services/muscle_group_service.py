from entities.muscle_group import MuscleGroup

from repositories.muscle_group_repository import (
    muscle_group_repository as default_muscle_group_repository
)

class MuscleGroupService:
    def __init__(self, muscle_group_repository=default_muscle_group_repository):
        self._muscle_group_repository = muscle_group_repository

    def get_all(self):
        return self._muscle_group_repository.get_all()

    def create(self, name):
        return self._muscle_group_repository.create(MuscleGroup(name=name))

    def delete(self, muscle_group):
        self._muscle_group_repository.delete(muscle_group=muscle_group)

muscle_group_service = MuscleGroupService()
