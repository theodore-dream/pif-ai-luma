import psycopg2
from uuid import uuid4
import time
from psycopg2 import Error
from psycopg2 import OperationalError


try:
    connection = psycopg2.connect(dbname="postgres",
                              host="db",
                              user="postgres",
                              password="raspberry",
                              port = "5432",
                              connect_timeout=3)

    connection.autocommit = True

    # Debugging information
    print("Connected to the Postgres database successfully")

    # Create a new database called "Poems" if it doesn't already exist
    cur = connection.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname='game'")
    exists = cur.fetchone()

    if exists:
        print("Database already exists")
    else:
        cur.execute("CREATE DATABASE game;")
        print("game Database created successfully")

    # Close the cursor and connection to "postgres"
    cur.close()
    connection.close()

    # Connect to the new "Poems" database
    connection = psycopg2.connect(dbname="game",
                              host="db",
                              user="postgres",
                              password="raspberry",
                              port = "5432",
                              connect_timeout=3)

    connection.autocommit = True

    # Debugging information
    print("Connected to the game database successfully")

    cursor = connection.cursor()
    # this line is to ensure UUID support is in place
    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    # check if the table exists
    cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='game')")
    table_exists = cursor.fetchone()[0]

    if table_exists:
        print("game already exists in PostgreSQL")
    else:
        # SQL query to create a new table
        create_table_query = '''CREATE TABLE game (session_id uuid DEFAULT uuid_generate_v4 (),
                              tstz timestamp DEFAULT current_timestamp,
                              prompt VARCHAR,
                              gametext VARCHAR,
                              player_optiona VARCHAR,
                              player_optionb VARCHAR,
                              danger NUMERIC(3, 0),
                              level NUMERIC(3, 0),
                              PRIMARY KEY (session_id));'''
        # Execute a command: this creates a new table
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL")

except OperationalError as e:
    print("Operational Error:", e)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

    # Debugging information
    print("PostgreSQL connection is closed")
