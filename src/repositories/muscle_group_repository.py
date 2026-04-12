from entities.muscle_group import MuscleGroup
from database.database_connection import get_database_connection


class MuscleGroupRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, muscle_group):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO muscle_groups (name) VALUES (?)",
            (muscle_group.name,)
        )
        self._connection.commit()
        muscle_group.id = cursor.lastrowid
        return muscle_group

    def get_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT id, name FROM muscle_groups")
        rows = cursor.fetchall()
        return [
            MuscleGroup(name=row["name"], muscle_group_id=row["id"])
            for row in rows
        ]

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM muscle_groups")
        self._connection.commit()


muscle_group_repository = MuscleGroupRepository(get_database_connection())
