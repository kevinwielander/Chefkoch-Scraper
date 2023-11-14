import base64

import psycopg2
import json

# Replace these with your database connection details
dbname = "recipes"
user = "root"
password = "root"
host = "localhost"
port = "5432"

# Replace this with your JSON file path
ingredients_set_file = "../analysis/ingredients_lemma_set.txt"

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()

    # Create the 'recipes' table if it doesn't exist
    create_table_query = """
       CREATE TABLE IF NOT EXISTS ingredients (
           id SERIAL PRIMARY KEY,
           name TEXT
       );
       """
    cursor.execute(create_table_query)
    connection.commit()

    # Load data from the JSON file
    with open(ingredients_set_file, 'r', encoding='utf-8') as file:
        # Iterate over each entry and insert into the table
        for line in file:

            # Insert the ingredient into the table
            insert_query = "INSERT INTO ingredients (name) VALUES (%s);"
            cursor.execute(insert_query, (line,))

        connection.commit()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
