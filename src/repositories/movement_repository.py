from entities.movement import Movement
from entities.muscle_group import MuscleGroup
from dto.movement_option import MovementOption
from database.database_connection import get_database_connection


class MovementRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_all_movement_options(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name FROM movements")
        rows = cursor.fetchall()

        return [MovementOption(movement_id=row["id"], movement_name=row["name"]) for row in rows]

    def create(self, movement):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO movements (name, primary_muscle_group_id) VALUES (?, ?)",
            (movement.name, movement.primary_muscle_group.id)
        )
        self._connection.commit()
        movement.id = cursor.lastrowid
        return movement

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM movements")
        self._connection.commit()

    def delete(self, movement):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM movements WHERE id = ?", (movement.id,))
        self._connection.commit()

    def get_all(self):
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


movement_repository = MovementRepository(get_database_connection())
