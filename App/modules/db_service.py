import psycopg2
from psycopg2 import Error

def test_db_connection():
    conn = None 
    try:
        conn = psycopg2.connect("dbname=poems user=postgres host=db port=5432 password=raspberry")
        print("Database connection successful!")
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
    finally:
        if conn:
            conn.close()

def save_poem_to_database(poem):
    try:
        connection = psycopg2.connect(
            dbname="poems",
            host="db",
            user="postgres",
            password="raspberry",
            port="5432",
            connect_timeout=3,
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO poetry (poem_contents) VALUES (%s)", (poem,)
        )
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, Error) as error:
        print("Error while saving poem to PostgreSQL", error)
