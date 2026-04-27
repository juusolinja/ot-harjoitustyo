from entities.muscle_group import MuscleGroup
from database.database_connection import get_database_connection


class MuscleGroupRepository:
    """Lihasryhmiin liittyvistä tietokantaoperaatioista vastaava luokka
    """

    def __init__(self, connection):
        """Luokan konstruktori

        Args:
            connection: Tietokantayhteyden Connection-olio
        """

        self._connection = connection

    def create(self, muscle_group):
        """Tallentaa lihasryhmän tietokantaan

        Args:
            muscle_group: Tallennettava lihasryhmä MuscleGroup-oliona

        Returns:
            Palauttaa tallennetun lihasryhmän MuscleGroup-oliona
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO muscle_groups (name) VALUES (?)",
            (muscle_group.name,)
        )
        self._connection.commit()
        muscle_group.id = cursor.lastrowid
        return muscle_group

    def get_all(self):
        """Palauttaa kaikki lihasryhmät

        Returns:
            Palauttaa listan MuscleGroup-olioita
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name FROM muscle_groups")
        rows = cursor.fetchall()
        return [
            MuscleGroup(name=row["name"], muscle_group_id=row["id"])
            for row in rows
        ]

    def delete(self, muscle_group):
        """Poistaa annetun lihasryhmän tietokannasta

        Args:
            muscle_group: Poistettava lihasryhmä MuscleGroup-oliona
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM muscle_groups WHERE id = ?", (muscle_group.id,))
        self._connection.commit()

    def delete_all(self):
        """Poistaa kaikki lihasryhmät tietokannasta
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM muscle_groups")
        self._connection.commit()

    def is_referred_to(self, muscle_group):
        """Tarkistaa viittaako tietokannassa mikään liike annettuun lihasryhmään

        Args:
            muscle_group: lihasryhmä MuscleGroup-oliona

        Returns:
            Palauttaa Boolean-arvon
        """

        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM movements
                WHERE primary_muscle_group_id = ?
            )
            """, (muscle_group.id,)
        )
        return cursor.fetchone()[0] == 1

muscle_group_repository = MuscleGroupRepository(get_database_connection())
