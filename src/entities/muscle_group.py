class MuscleGroup:
    """Luokka, joka kuvaa yksittäistä lihasryhmää

    Attributes:
        id: Kokonaisluku, joka kuvaa lihasryhmän id:tä.
        name: Merkkijonoarvo, joka kuvaa lihasryhmän nimeä.
    """
    def __init__(self, name, muscle_group_id=None):
        """Luokan konstruktori, joka luo uuden lihasryhmän.

        Args:
            name: Merkkijonoarvo, joka kuvaa lihasrymän nimeä.
            muscle_group_id:
                Vapaaehtoinen, oletusarvoltaan None.
                Kokonaisluku, joka kuvaa lihasryhmän id:tä.
        """
        self.id = muscle_group_id
        self.name = name
