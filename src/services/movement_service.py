from entities.movement import Movement

from repositories.movement_repository import (
    movement_repository as default_movement_repository
)

from repositories.muscle_group_repository import (
    muscle_group_repository as default_muscle_group_repository
)

class MovementService:
    def __init__(self,
                 movement_repository=default_movement_repository,
                 muscle_group_repository=default_muscle_group_repository
                ):
        self._movement_repository = movement_repository
        self._muscle_group_repository = muscle_group_repository

    def get_all(self):
        return self._movement_repository.get_all()

    def get_all_movement_options(self):
        return self._movement_repository.get_all_movement_options()

    def create(self, name, muscle_group):
        return self._movement_repository.create(
            Movement(name=name, primary_muscle_group=muscle_group)
        )

    def delete(self, movement):
        self._movement_repository.delete(movement=movement)

movement_service = MovementService()
