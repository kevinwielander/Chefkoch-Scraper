import psycopg2

from utils.import_db_ingredient import import_db_ingredient
import os

from utils.import_db_recipe import import_db_recipe


def setup_db_connection():
    dbname = os.environ['dbname']
    user = os.environ['user']
    password = os.environ['password']
    host = os.environ['host']
    port = os.environ['port']
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()
    return cursor, connection


def terminate_db_connection(cursor, connection):
    cursor.close()
    connection.close()


try:
    cursorDB, connectionDB = setup_db_connection()
    import_db_ingredient(cursorDB, connectionDB)
    import_db_recipe(cursorDB, connectionDB)
    terminate_db_connection(cursorDB, connectionDB)
except Exception as e:
    print(f"Error: {e}")
