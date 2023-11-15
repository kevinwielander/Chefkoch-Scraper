from analysis.german_lemmatizer import create_lemmatized_iingredients_set
from analysis.ingredient_extractor import extract_ingredients
from utils.db_operations import setup_db_connection, terminate_db_connection
from utils.transform_json_to_database_table import import_db_recipe_ingredient, import_db_ingredient, import_db_recipe
from utils.fetch_json import download_and_save_recipes

import traceback


try:
    print("---- START DOWNLOADING RECIPES! ----")
    download_and_save_recipes()
    print("--- START EXTRACTING INGREDIENTS FROM RECIPES JSON ---")
    extract_ingredients()
    print("--- START LEMMATIZATION OF EXTRACTED INGREDIENTS ---")
    create_lemmatized_iingredients_set()
    cursorDB, connectionDB = setup_db_connection()
    print("---- START INGREDIENTS! ----")
    import_db_ingredient(cursorDB, connectionDB)
    print("---- START RECIPES! ---- ")
    import_db_recipe(cursorDB, connectionDB)
    print("---- START RECIPES & INGREDIENTS! ----")
    import_db_recipe_ingredient(cursorDB, connectionDB)
    terminate_db_connection(cursorDB, connectionDB)
    print("---- DONE :) ----")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
