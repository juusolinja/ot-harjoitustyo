import os
import json
from database.database_connection import get_database_connection

dirname = os.path.dirname(__file__)
schema_path = os.path.join(dirname, "schema.sql")
see_movements_path = os.path.join(dirname, "seed_movements.json")


def drop_tables(connection):
    cursor = connection.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS set_entries;
        DROP TABLE IF EXISTS movement_muscle_groups;
        DROP TABLE IF EXISTS movements;
        DROP TABLE IF EXISTS muscle_groups;
        DROP TABLE IF EXISTS workouts;        
    """)
    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()
    with open(schema_path, encoding="utf-8") as f:
        schema = f.read()
    cursor.executescript(schema)
    connection.commit()


def seed_movements(connection):
    cursor = connection.cursor()
    with open(see_movements_path, encoding="utf-8") as f:
        movements = json.load(f)
    try:
        cursor.execute("BEGIN")
        for movement in movements:
            cursor.execute(
                "INSERT OR IGNORE INTO muscle_groups (name) VALUES (?)",
                (movement["primary_muscle_group"],)
            )
            cursor.execute(
                "SELECT id FROM muscle_groups WHERE name = ?",
                (movement["primary_muscle_group"],)
            )
            muscle_group_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT OR IGNORE INTO movements (name, primary_muscle_group_id) VALUES (?, ?)",
                (movement["name"], muscle_group_id)
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise


def initialize_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)
    seed_movements(connection)


if __name__ == "__main__":
    initialize_database()
