import os
from dotenv import load_dotenv
import psycopg2


def setup_db_connection():
    load_dotenv()
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


def execute_query(cursor, file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read()
        cursor.execute(sql_query)


def execute_parameterized_query(cursor, file_path, params):
    with open(file_path, 'r') as file:
        sql_query = file.read()
        cursor.execute(sql_query, params)
