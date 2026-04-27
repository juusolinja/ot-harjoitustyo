from entities.muscle_group import MuscleGroup

from repositories.muscle_group_repository import (
    muscle_group_repository as default_muscle_group_repository
)

class MuscleGroupService:
    """Lihasryhmiin liittyvästä logiikasta vastaava luokka
    """

    def __init__(self, muscle_group_repository=default_muscle_group_repository):
        """Luokan konstruktori

        Args:
            muscle_group_repository:
                Vapaaehtoinen, oletusarvoltaan MuscleGroupRepository-olio
                Olio, jolla on MuscleGroupRepository-luokkaa vastaavat metodit
        """

        self._muscle_group_repository = muscle_group_repository

    def get_all(self):
        """Palauttaa kaikki lihasryhmät

        Returns:
            Palauttaa listan MuscleGroup-olioita
        """

        return self._muscle_group_repository.get_all()

    def create(self, name):
        """Luo lihasryhmän

        Args:
            name: Merkkijonoarvo, joka kuvaa lihasryhmän nimeä

        Returns:
            Palauttaa luodun lihasryhmön MuscleGroup-oliona
        """

        return self._muscle_group_repository.create(MuscleGroup(name=name))

    def delete(self, muscle_group):
        """Poistaa lihasryhmän

        Args:
            muscle_group: Poistettava lihasryhmä MuscleGroup-oliona
        """

        self._muscle_group_repository.delete(muscle_group=muscle_group)

    def is_referred_to(self, muscle_group):
        """Tarkistaa viittaako mikään liike annettuun lihasryhmään

        Args:
            muscle_group: Tarkistettva lihasryhmä MuscleGroup-oliona

        Returns:
            Boolean-arvo, sen mukaan viittaako tietokannassa yksikään liike annettuun lihasryhmään
        """

        return self._muscle_group_repository.is_referred_to(muscle_group)

muscle_group_service = MuscleGroupService()
