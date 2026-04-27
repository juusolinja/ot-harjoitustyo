class Movement:
    """Luokka, joka kuvaa yksittäistä liikettä

    Attributes:
        name: Merkkijonoarvo, joka kuvaa liikkeen nimeä.
        primary_muscle_group: MuscleGroup-olio, joka kuvaa liikkeen päälihasryhmää.
        id: Kokonaisluku, joka kuvaa liikkeen id:tä
    """
    def __init__(self, name, primary_muscle_group, movement_id=None):
        """Luokan konstruktori, joka luo uuden liikkeen.

        Args:
            name: Merkkijonoarvo, joka kuvaa liikkeen nimeä.
            primary_muscle_group: MuscleGroup-olio, joka kuvaa liikkeen päälihasryhmää.
            movement_id:
                Vapaaehtoinen, oletusarvoltaan None.
                Kokonaisluku, joka kuvaa liikkeen id:tä
        """
        self.name = name
        self.primary_muscle_group = primary_muscle_group
        self.id = movement_id
