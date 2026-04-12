from entities.workout import Workout
from entities.set_entry import SetEntry
from entities.movement import Movement
from entities.muscle_group import MuscleGroup
from dto.workout_summary import WorkoutSummary
from database.database_connection import get_database_connection


class WorkoutRepository:
    def __init__(self, connection):
        self._connection = connection

    def delete_all(self):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts")
        self._connection.commit()

    def get_all_workout_summaries(self):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, date, title, duration FROM workouts ORDER BY date DESC, id DESC")
        rows = cursor.fetchall()

        return [
            WorkoutSummary(
                workout_id=row["id"],
                date=row["date"],
                title=row["title"],
                duration=row["duration"]
            )
            for row in rows
        ]

    def get_by_id(self, workout_id):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, date, title, notes, duration FROM workouts WHERE id = ?", (workout_id,))
        workout_row = cursor.fetchone()
        if workout_row is None:
            return None
        cursor.execute(
            """
            SELECT
                m.id AS mv_id,
                m.name AS mv_name,
                mg.id AS mg_id,
                mg.name AS mg_name,
                s.id, s.reps, s.weight, s.rir
            FROM set_entries s
            JOIN movements m ON m.id = s.movement_id
            JOIN muscle_groups mg ON mg.id = m.primary_muscle_group_id
            WHERE s.workout_id = ?
            ORDER BY s.set_order
            """,
            (workout_id,)
        )
        set_rows = cursor.fetchall()

        sets = [
            SetEntry(
                movement=Movement(
                    name=row["mv_name"],
                    movement_id=row["mv_id"],
                    primary_muscle_group=MuscleGroup(
                        name=row["mg_name"],
                        muscle_group_id=row["mg_id"]
                    )
                ),
                reps=row["reps"],
                weight=row["weight"],
                rir=row["rir"]
            )
            for row in set_rows
        ]

        return Workout(
            title=workout_row["title"],
            date=workout_row["date"],
            notes=workout_row["notes"],
            workout_id=workout_row["id"],
            duration=workout_row["duration"],
            sets=sets
        )

    def create(self, workout):
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO workouts (title, date, duration, notes) values (?, ?, ?, ?)",
            (workout.title, workout.date, workout.duration, workout.notes)
        )
        workout.id = cursor.lastrowid
        for i, s in enumerate(workout.sets, start=1):
            cursor.execute(
                """
                INSERT INTO set_entries (workout_id, movement_id, set_order, reps, weight, rir)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (workout.id, s.movement.id, i, s.reps, s.weight, s.rir)
            )
        self._connection.commit()
        return workout

    def update(self, workout):
        cursor = self._connection.cursor()
        try:
            cursor.execute("BEGIN")
            cursor.execute(
                "UPDATE workouts SET title = ?, date = ?, duration = ?, notes = ? WHERE id = ?",
                (workout.title, workout.date,
                 workout.duration, workout.notes, workout.id)
            )
            cursor.execute(
                "DELETE FROM set_entries WHERE workout_id = ?", (workout.id,))
            for i, s in enumerate(workout.sets, start=1):
                cursor.execute(
                    """
                    INSERT INTO set_entries (workout_id, movement_id, set_order, reps, weight, rir)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (workout.id, s.movement.id, i, s.reps, s.weight, s.rir)
                )
            self._connection.commit()
            return workout
        except Exception:
            self._connection.rollback()
            raise

    def delete(self, workout):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM workouts WHERE id = ?", (workout.id,))
        self._connection.commit()


workout_repository = WorkoutRepository(get_database_connection())
