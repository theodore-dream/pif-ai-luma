import psycopg2
from psycopg2 import Error

def test_db_connection():
    conn = None
    try:
        conn = psycopg2.connect("dbname=game user=postgres host=db port=5432 password=raspberry")
        print("Database connection successful!")
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    finally:
        if conn:
            conn.close()

def write_to_database(session_id, level, danger, column, value):
    try:
        connection = psycopg2.connect(
            dbname="game",
            host="db",
            user="postgres",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        cursor.execute(
            f"UPDATE game SET {column} = %s WHERE session_id = %s", (value, session_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        print("Error while updating column in PostgreSQL", error)

def read_from_database(session_id, level, danger, column):
    try:
        connection = psycopg2.connect(
            dbname="game",
            host="db",
            user="postgres",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT {column} FROM game WHERE session_id = %s", (session_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except (Exception, Error) as error:
        print("Error while reading column from PostgreSQL", error)
        return None

# Example usage:
# write_to_database(session_id, 'prompt', 'your_prompt_here')
# write_to_database(session_id, 'player-optiona', 'option_a_here')
# write_to_database(session_id, 'player-optionb', 'option_b_here')
# write_to_database(session_id, 'danger', 42.0)
#
# prompt = read_from_database(session_id, 'prompt')
# player_optiona = read_from_database(session_id, 'player-optiona')
# player_optionb = read_from_database(session_id, 'player-optionb')
# danger = read_from_database(session_id, 'danger')