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
                              port = "5432")

    # Create a new database called "Poems"
    connection.autocommit = True
    cur = connection.cursor()
    cur.execute("CREATE DATABASE poems;")
    print("Database created successfully")
    connection.close()

 # Connect to the new "Poems" database
    connection = psycopg2.connect(dbname="poems",
                              host="db",
                              user="postgres",
                              password="raspberry",
                              port = "5432")

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = '''CREATE TABLE poetry (poem_id uuid DEFAULT uuid_generate_v4 (),
                          tstz timestamp DEFAULT current_timestamp,
                          poem_contents VARCHAR NOT NULL,
                          PRIMARY KEY (poem_id));'''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except OperationalError as e:
    print("Error:", e)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)


finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
    print("PostgreSQL connection is closed")