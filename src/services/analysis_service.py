from repositories.workout_repository import (
    workout_repository as default_workout_repository
)
from repositories.muscle_group_repository import (
    muscle_group_repository as default_muscle_group_repository
)
from date_utils import get_current_week_range

class AnalysisService:
    """Treenin analysointiin liittyvästä logiikasta vastaava luokka
    """

    def __init__(self, workout_repository=default_workout_repository,
                       muscle_group_repository=default_muscle_group_repository):
        """Luokan konstruktori

        Args:
            workout_repository:
                Vapaaehtoinen, oletusarvoltaan WorkoutRepository-olio
                Olio, jolla on WorkoutRepository-luokkaa vastaavat metodit
            muscle_group_repository:
                Vapaaehtoinen, oletusarvoltaan MuscleGroupRepository-olio
                Olio, jolla on MuscleGroupRepository-luokkaa vastaavat metodit
        """

        self._workout_repository = workout_repository
        self._muscle_group_repository = muscle_group_repository

    def get_current_week_volumes(self):
        """Palauttaa jokaiselle lihasryhmälle tehtyjen sarjojen lukumäärän nykyisellä viikolla

        Returns:
            Palauttaa kirjaston,
            jossa avaimena on lihasryhmän nimi ja arvona tehtyjen sarjojen lukumäärä
        """

        monday, sunday = get_current_week_range()
        current_week_workouts = self._workout_repository.get_all_from_timespan(monday, sunday)
        all_muscle_groups = self._muscle_group_repository.get_all()
        volumes = {mg.name: 0 for mg in all_muscle_groups}
        for w in current_week_workouts:
            for s in w.sets:
                volumes[s.movement.primary_muscle_group.name] += 1
        return volumes


analysis_service = AnalysisService()
