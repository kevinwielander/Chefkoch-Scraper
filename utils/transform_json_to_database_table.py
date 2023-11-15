import base64

import psycopg2
import json
import spacy
import re

from db_operations import execute_parameterized_query, execute_query

list_jsons = [
    '../recipes_data/breakfast.json',
    '../recipes_data/dessert.json',
    '../recipes_data/main_dish.json',
    '../recipes_data/side_dish.json',
    '../recipes_data/snack.json',
    '../recipes_data/starter.json'
]


def import_db_recipe(cursor, connection):
    # Create the 'recipes' table if it doesn't exist
    execute_query(cursor, 'queries/create_recipe_table.sql')
    connection.commit()

    for json_file_path in list_jsons:

        # Load data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data_list = json.load(file)

        # Iterate over each entry and insert into the table
        for entry in json_data_list:
            # print(entry.get("Preparation time"))

            image_data = None
            base64_image = entry.get("Image", "")
            if base64_image:
                try:
                    image_data = base64.b64decode(base64_image)
                except Exception as e:
                    #print(f"Error decoding image for {entry.get('Title', 'Unknown')}: {e}")
                    image_data = None  # Or handle the error as needed

            modified_entry = {
                "title": entry.get("Title", ""),
                "url": entry.get("URL", ""),
                "preparation_time": entry.get("Preparation time", "").split('\n')[1] if '\n' in entry.get(
                    "Preparation time", "") else entry.get("Preparation time", ""),
                # Handling 'Calories' which might be None
                "calories": (entry.get("Calories", "") or "").split('\n')[1] if '\n' in (
                        entry.get("Calories", "") or "") else entry.get(
                    "Calories", ""),
                "description": entry.get("Description", ""),
                "portions": entry.get("Portions", ""),
                "image": image_data,
                "category": "dessert"
            }
            #print(modified_entry.get("title"))

            # Insert the JSON data into the table
            execute_parameterized_query(cursor, 'queries/insert_recipe_entry.sql', tuple(modified_entry.values()))
        connection.commit()


def import_db_ingredient(cursor, connection):
    ingredients_set_file = "../analysis/ingredients_lemma_set.txt"
    execute_query(cursor, 'queries/create_ingredient_table.sql')
    connection.commit()

    # Load data from the JSON file
    with open(ingredients_set_file, 'r', encoding='utf-8') as file:
        # Iterate over each entry and insert into the table
        for line in file:
            ingredient_name = line.replace('\n', "")
            # Insert the ingredient into the table
            execute_parameterized_query(cursor, 'queries/insert_ingredient_entry.sql', (ingredient_name,))

        connection.commit()


def import_db_recipe_ingredient(cursor, connection):
    nlp = spacy.load('de_core_news_md')

    execute_query(cursor, 'queries/create_recipe_ingredient_table.sql')
    connection.commit()

    for json_file_path in list_jsons:
        # Load data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data_list = json.load(file)

        # Iterate over each entry and insert into the table
        for entry in json_data_list:
            title = entry.get("Title", "")
            ingredients = entry.get("Ingredients", "")

            execute_parameterized_query(cursor, 'queries/retrieve_recipe_id.sql', (title,))
            recipe_id = cursor.fetchone()

            if not recipe_id:
                continue

            recipe_id = recipe_id[0]
            #print("recipe " + str(recipe_id))

            for ingredient in ingredients:
                ingredient_name = ingredient.get("ingredient", "")
                ingredient_amount = ingredient.get("amount", "")

                cleaned_ingredient = re.sub(r'\s*\(.*\)|\s.*', '', ingredient_name)
                cleaned_string = cleaned_ingredient.replace(',', '')
                ingredient_lemma = nlp(cleaned_string).text
                execute_parameterized_query(cursor, 'queries/retrieve_ingredient_id.sql', (ingredient_lemma,))
                ingredient_id = cursor.fetchone()
                if not ingredient_id:
                    continue

                ingredient_id = ingredient_id[0]
                #print("ingredient " + str(ingredient_id))

                # Insert the ingredient into the table
                execute_parameterized_query(cursor, 'queries/insert_recipe_ingredients_entry.sql',
                                            (recipe_id, ingredient_id, ingredient_name, ingredient_amount))
    # Commit the transaction after all entries are inserted
    connection.commit()
