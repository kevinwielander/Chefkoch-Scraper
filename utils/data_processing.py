import json


def extract_units_and_ingredients(json_file, output_file):
    """
    Reads a JSON file containing recipe data and extracts unique units of amounts
    along with the ingredients associated with each unit. Writes the results to an output file.

    :param json_file: Path to the JSON file
    :param output_file: Path to the output file where the results will be written
    """
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        recipes = json.load(file)

    # Dictionary to store units and their ingredients
    units_and_ingredients = {}

    # Iterate over each recipe
    for recipe in recipes:
        # Iterate over each ingredient in the recipe
        for ingredient in recipe['Ingredients']:
            amount = ingredient['amount']
            ingredient_name = ingredient['ingredient']

            # Extract the unit from the amount
            unit = ''.join(filter(str.isalpha, amount))

            # Skip if there is no unit or ingredient
            if not unit or not ingredient_name:
                continue

            # Add the ingredient to the set of ingredients for the unit
            if unit not in units_and_ingredients:
                units_and_ingredients[unit] = {ingredient_name}
            else:
                units_and_ingredients[unit].add(ingredient_name)

    # Write the units and ingredients to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for unit, ingredients in units_and_ingredients.items():
            file.write(f"Unit: {unit}, Ingredients: {list(ingredients)}\n")  # Using a list for JSON serialization


# Usage
extract_units_and_ingredients('../recipes_data/breakfast_page_22.json', '../analysis/units_and_ingredients.txt')
