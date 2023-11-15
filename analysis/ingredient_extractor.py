import json


def extract_ingredients():
    """
    Reads a JSON file containing recipe data and extracts ingidients and also stores the amounts
    Writes the results to an output file.

    :param json_file: Path to the JSON file
    """
    # Read the JSON file

    list_jsons = [
        '../recipes_data/breakfast.json',
        '../recipes_data/dessert.json',
        '../recipes_data/main_dish.json',
        '../recipes_data/side_dish.json',
        '../recipes_data/snack.json',
        '../recipes_data/starter.json'
    ]

    # Dictionary to store ingredients
    occurrences_of_ingredients = {}

    for json_file in list_jsons:
        with open(json_file, 'r', encoding='utf-8') as file:
            recipes = json.load(file)


        # Iterate over each recipe
        for recipe in recipes:
            # Iterate over each ingredient in the recipe
            for ingredient in recipe['Ingredients']:
                ingredient_name = ingredient['ingredient']
                amount = ingredient['amount']

                # Skip if there is no amount or ingredient
                if not amount or not ingredient_name:
                    continue

                # Add the ingredient to the set of ingredients for the unit
                if ingredient_name not in occurrences_of_ingredients:
                    occurrences_of_ingredients[ingredient_name] = 1
                else:
                    occurrences_of_ingredients[ingredient_name] += 1

        sorted_ingredients = sorted(occurrences_of_ingredients.items(), key=lambda x: x[1], reverse=True)

    # Write the units and ingredients to the output file
    with open('analysis/ingredients.txt', 'w', encoding='utf-8') as file:
        for ingredient, count in sorted_ingredients:
            file.write(f"{ingredient}\n")

