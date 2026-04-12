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


movement_repository = MovementRepository(get_database_connection())
