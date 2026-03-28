from entities.workout import Workout
from database.database_connection import get_database_connection

def get_workout_by_row(row):
    return Workout(row["date"], row["notes"], row["id"]) if row else None

class WorkoutRepository:
    def __init__(self, connection):
        self._connection = connection

    def get_all(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM workouts")
        rows = cursor.fetchall()

        return list(map(get_workout_by_row, rows))
    
    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts")
        self._connection.commit()

    def create(self, workout):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO workouts (date, notes) values (?, ?)",
            (workout.date, workout.notes)
        )
        self._connection.commit()
        
        return workout

    
workout_repository = WorkoutRepository(get_database_connection())