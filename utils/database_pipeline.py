from db_operations import setup_db_connection, terminate_db_connection
from transform_json_to_database_table import import_db_recipe_ingredient, import_db_ingredient, import_db_recipe
from fetch_json import download_and_save_recipes

import traceback


try:
    print("---- START DOWNLOADING RECIPES! ----")
    download_and_save_recipes()
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
