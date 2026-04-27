from entities.movement import Movement

from repositories.movement_repository import (
    movement_repository as default_movement_repository
)

from repositories.muscle_group_repository import (
    muscle_group_repository as default_muscle_group_repository
)

class MovementService:
    """Liikkeisiin liittyvästä logiikasta vastaava luokka
    """

    def __init__(self,
                 movement_repository=default_movement_repository,
                 muscle_group_repository=default_muscle_group_repository
                ):
        """Luokan konstruktori

        Args:
            movement_repository:
                Vapaaehtoinen, oletusarvoltaan MovementRepository-olio
                Olio, jolla on MovementRepository-luokkaa vastaavat metodit
            muscle_group_repository:
                Vapaaehtoinen, oletusarvoltaan MuscleGroupRepository-olio
                Olio, jolla on MuscleGroupRepository-luokkaa vastaavat metodit
        """

        self._movement_repository = movement_repository
        self._muscle_group_repository = muscle_group_repository

    def get_all(self):
        """Palauttaa kaikki liikkeet

        Returns:
            Palauttaa listan Movement-olioita
        """

        return self._movement_repository.get_all()

    def get_all_movement_options(self):
        """Palauttaa kaikki liikevaihtoehdot

        Returns:
            Palauttaa listan MovementOption-olioita
        """

        return self._movement_repository.get_all_movement_options()

    def create(self, name, muscle_group):
        """Luo uuden liikkeen

        Args:
            name: Merkkijonoarvo, joka kuvaa liikkeen nimeä
            muscle_group: MuscleGroup-olio, joka kuvaa liikken päälihasryhmää

        Returns:
            Palauttaa luodun liikkeen Movement-oliona
        """

        return self._movement_repository.create(
            Movement(name=name, primary_muscle_group=muscle_group)
        )

    def delete(self, movement):
        """Poistaa liikkeen

        Args:
            movement: Poistettava liike Movement-oliona
        """

        self._movement_repository.delete(movement=movement)

    def is_referred_to(self, movement):
        """Tarkistaa viittaako mikään sarja annettuun liikkeeseen

        Args:
            movement: Tarkistettva liike Movement-oliona

        Returns:
            Boolean-arvo, sen mukaan viittaako tietokannassa yksikään sarja annettuun liikkeeseen
        """

        return self._movement_repository.is_referred_to(movement)

movement_service = MovementService()
