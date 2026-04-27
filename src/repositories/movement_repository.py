from entities.movement import Movement
from entities.muscle_group import MuscleGroup
from dto.movement_option import MovementOption
from database.database_connection import get_database_connection


class MovementRepository:
    """Liikkeisiin liittyvistä tietokantaoperaatioista vastaava luokka
    """

    def __init__(self, connection):
        """Luokan konstruktori

        Args:
            connection: Tietokantayhteyden Connection-olio
        """

        self._connection = connection

    def get_all_movement_options(self):
        """Palauttaa kaikki liikevaihtoehdot

        Returns:
            Palauttaa listan MovementOption-olioita
        """

        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name FROM movements")
        rows = cursor.fetchall()

        return [MovementOption(movement_id=row["id"], movement_name=row["name"]) for row in rows]

    def create(self, movement):
        """Tallentaa liikkeen tietokantaan

        Args:
            movement: Tallennettava liike Movement-oliona

        Returns:
            Tallennettu liike Movement-oliona
        """

        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO movements (name, primary_muscle_group_id) VALUES (?, ?)",
            (movement.name, movement.primary_muscle_group.id)
        )
        self._connection.commit()
        movement.id = cursor.lastrowid
        return movement

    def delete_all(self):
        """Poistaa kaikki liikkeet tietokannasta
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM movements")
        self._connection.commit()

    def delete(self, movement):
        """Poistaa liikkeen tietokannasta

        Args:
            movement: Poistettava liike Movement-oliona
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM movements WHERE id = ?", (movement.id,))
        self._connection.commit()

    def get_all(self):
        """Palauttaa kaikki liikkeet

        Returns:
            Palauttaa liikkeet listana Movement-olioita
        """
        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT mv.id, mv.name, mg.id AS mg_id, mg.name AS mg_name
            FROM movements mv
            JOIN muscle_groups mg ON mv.primary_muscle_group_id = mg.id
            ORDER BY mv.name
            """
        )
        return [
            Movement(name=row["name"],
                     movement_id=row["id"],
                     primary_muscle_group=MuscleGroup(
                         name=row["mg_name"],
                         muscle_group_id=row["mg_id"]
                     )
            )
            for row in cursor.fetchall()
        ]

    def is_referred_to(self, movement):
        """Tarkistaa viittaako tietokannassa mikään sarja annettuun liikkeeseen

        Args:
            movement: Liike Movement-oliona

        Returns:
            Boolean-arvo riippuen siitä viittaako tietokannassa mikään sarja annettuun liikkeeseen
        """

        cursor = self._connection.cursor()
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM set_entries
                WHERE movement_id = ?
            )
            """, (movement.id,)
        )
        return cursor.fetchone()[0] == 1


movement_repository = MovementRepository(get_database_connection())
