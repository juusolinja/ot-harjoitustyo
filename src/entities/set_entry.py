class SetEntry:
    """Luokka, joka kuvaa yksittäistä sarjaa

        Attributes:
            movement: Movement-olio, joka kuvaa sarjan liikettä.
            reps: Kokonaisluku, joka kuvaa toistojen määrää.
            weight: Liukuluku, joka kuvaa painon määrää.
            rir: Kokonaisluku, joka kuvaa sarjan haastavuutta.
    """

    def __init__(self, movement, reps, weight, rir):
        """Luokan konstruktori, joka luo uuden sarjan

        Args:
            movement: Movement-olio, joka kuvaa sarjan liikettä.
            reps: Kokonaisluku, joka kuvaa toistojen määrää.
            weight: Liukuluku, joka kuvaa painon määrää.
            rir: Kokonaisluku, joka kuvaa sarjan haastavuutta.
        """

        self.movement = movement
        self.reps = reps
        self.weight = weight
        self.rir = rir
