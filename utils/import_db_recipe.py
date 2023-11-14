import base64

import psycopg2
import json
import spacy
import re

nlp = spacy.load('de_core_news_md')


def import_db_recipe(cursor, connection):
    # Create the 'recipes' table if it doesn't exist
    create_table_query = """
       CREATE TABLE IF NOT EXISTS recipes (
           id SERIAL PRIMARY KEY,
           title TEXT,
           url TEXT,
           preparation_time TEXT,
           calories TEXT,
           description TEXT,
           portions TEXT,
           image BYTEA,
           category TEXT
       );
       """
    cursor.execute(create_table_query)
    connection.commit()

    list_jsons = [
        '../recipes_data/breakfast.json',
        '../recipes_data/dessert.json',
        '../recipes_data/main_dish.json',
        '../recipes_data/side_dish.json',
        '../recipes_data/snack.json',
        '../recipes_data/starter.json'
    ]

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
                    print(f"Error decoding image for {entry.get('Title', 'Unknown')}: {e}")
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
            print(modified_entry.get("title"))

            # Insert the JSON data into the table
            insert_query = """
                    INSERT INTO recipes (title, url, preparation_time, calories, description, portions, image, category)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
            cursor.execute(insert_query, tuple(modified_entry.values()))

            print("executed!")

        # Commit the transaction after all entries are inserted
        connection.commit()
