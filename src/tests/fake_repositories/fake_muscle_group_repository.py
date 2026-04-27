class FakeMuscleGroupRepository:
    def __init__(self, muscle_groups=None):
        self.muscle_groups = muscle_groups or []
        self._next_id = 1

    def create(self, muscle_group):
        muscle_group.id = self._next_id
        self._next_id += 1
        self.muscle_groups.append(muscle_group)
        return muscle_group

    def get_all(self):
        return self.muscle_groups

    def delete(self, muscle_group):
        self.muscle_groups = [mg for mg in self.muscle_groups if mg.id != muscle_group.id]

    def delete_all(self):
        self.muscle_groups = []
        self._next_id = 1
