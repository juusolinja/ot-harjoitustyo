class Workout:
    """Luokka, joka kuvaa yksittäistä treeniä

        Attributes:
            title: Merkkijonoarvo, joka kuvaa treenin nimeä.
            date: Merkkijonoarvo, joka kuvaa treenin päivämäärää.
            notes: Merkkijonoarvo, joka kuvaa treenin muistiinpanoja.
            id: Kokonaisluku, joka kuvaa treenin id:tä.
            duration: Kokonaisluku, joka kuvaa treenin kestoa.
            sets: Lista SetEntry-olioita, joka kuvaa treenissä tehtyjä sarjoja.

    """
    def __init__(self, title, date, sets, notes=None, workout_id=None, duration=None):
        """Luokan konstruktori, joka luo uuden treenin

        Args:
            title: Merkkijonoarvo, joka kuvaa treenin nimeä.
            date: Merkkijonoarvo, joka kuvaa treenin päivämäärää.
            notes:
                Vapaaehtoinen, oletusarvoltaan None.
                Merkkijonoarvo, joka kuvaa treenin muistiinpanoja.
            workout_id:
                Vapaaehtoinen, oletusarvoltaan None.
                Kokonaisluku, joka kuvaa treenin id:tä.
            duration:
                Vapaaehtoinen, oletusarvoltaan None.
                Kokonaisluku, joka kuvaa treenin kestoa.
            sets: Lista SetEntry-olioita, joka kuvaa treenissä tehtyjä sarjoja.
        """
        
        self.title = title
        self.date = date
        self.notes = notes
        self.id = workout_id
        self.duration = duration
        self.sets = sets if sets is not None else []
