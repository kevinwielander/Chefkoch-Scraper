import base64
import os
import psycopg2
import json



def import_db_ingredient(cursor, connection):
    ingredients_set_file = "../analysis/ingredients_lemma_set.txt"
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
            ingredient_name = line.replace('\n', "")

            # Insert the ingredient into the table
            insert_query = "INSERT INTO ingredients (name) VALUES (%s);"
            cursor.execute(insert_query, (ingredient_name,))

        connection.commit()
