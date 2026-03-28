from database.database_connection import get_database_connection
import os

dirname = os.path.dirname(__file__)
schema_path = os.path.join(dirname, "schema.sql")

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS workouts;
    """)
    connection.commit()
    


def create_tables(connection):
    cursor = connection.cursor()
    with open(schema_path, "r") as f:
        schema = f.read()
    cursor.executescript(schema)
    connection.commit()


def initialize_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()