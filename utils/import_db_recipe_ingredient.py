import base64

import psycopg2
import json
import spacy
import re
nlp = spacy.load('de_core_news_md')

# Replace these with your database connection details
dbname = "recipes"
user = "root"
password = "root"
host = "localhost"
port = "5432"

list_jsons = [
    '../recipes_data/breakfast.json',
    '../recipes_data/dessert.json',
    '../recipes_data/main_dish.json',
    '../recipes_data/side_dish.json',
    '../recipes_data/snack.json',
    '../recipes_data/starter.json'
]

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

    #Create the 'recipes' table if it doesn't exist
    create_table_query = """
       CREATE TABLE IF NOT EXISTS recipe_ingredient (
           id SERIAL PRIMARY KEY,
           recipe_id INTEGER,
           ingredient_id INTEGER,
           info TEXT,
           amount TEXT,
           FOREIGN KEY (recipe_id) REFERENCES recipes(id),
           FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) 
       );
       """
    cursor.execute(create_table_query)
    connection.commit()

    for json_file_path in list_jsons:
        # Load data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data_list = json.load(file)

        # Iterate over each entry and insert into the table
        for entry in json_data_list:
            title = entry.get("Title", "")
            ingredients = entry.get("Ingredients", "")

            retrieve_recipe_id_query = "SELECT id  FROM recipes WHERE title = %s;"
            cursor.execute(retrieve_recipe_id_query, (title,))
            recipe_id = cursor.fetchone()

            if not recipe_id:
                continue

            recipe_id= recipe_id[0]
            print("recipe " + str(recipe_id))

            for ingredient in ingredients:
                ingredient_name = ingredient.get("ingredient", "")
                ingredient_amount = ingredient.get("amount", "")

                cleaned_ingredient = re.sub(r'\s*\(.*\)|\s.*', '', ingredient_name)
                cleaned_string = cleaned_ingredient.replace(',', '')
                ingredient_lemma = nlp(cleaned_string).text

                retrieve_ingredient_id_query = "SELECT id  FROM ingredients WHERE name = %s;"
                cursor.execute(retrieve_ingredient_id_query, (ingredient_lemma,))
                ingredient_id = cursor.fetchone()
                if not ingredient_id:
                    continue

                ingredient_id= ingredient_id[0]
                print("ingredient " + str(ingredient_id))

                # Insert the ingredient into the table
                insert_query = """INSERT INTO recipe_ingredient (recipe_id,ingredient_id, info,amount)
                 VALUES (%s, %s, %s, %s);"""
                cursor.execute(insert_query, (recipe_id,ingredient_id, ingredient_name, ingredient_amount))

    # Commit the transaction after all entries are inserted
    connection.commit()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
