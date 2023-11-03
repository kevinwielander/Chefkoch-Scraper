import base64

import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import json

# author: Cveta, Kevin
# TU Wien, 2023

# Base URL
base_url = 'https://www.chefkoch.de/'
max_page = 2
# Paths for different meal types
meal_paths = {
    'breakfast': 'rs/s$page$t53/Fruehstueck-Rezepte.html',
    #'snack': 'rs/s$page$t71/Snack-Rezepte.html',
    #'dessert': 'rs/s$page$t90/Dessert-Rezepte.html',
    #'side_dish': 'rs/s$page$t36/Beilage-Rezepte.html',
    #'starter': 'rs/s$page$t19/Vorspeise-Rezepte.html',
    #'main_dish': 'rs/s$page$t21/Hauptspeise-Rezepte.html'
}

# Add the base URL to each path
full_urls = {meal: base_url + path for meal, path in meal_paths.items()}


for meal, url in full_urls.items():
    recipe_data_list = []
    for i in range(max_page):
        url_current = url.replace('$page$', str(i))
        response = requests.get(url_current)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            recipe_links = [link['href'] for link in soup.find_all('a', class_='ds-recipe-card__link ds-teaser-link')]

            for link in recipe_links:
                print(link)
                recipe_response = requests.get(link)
                soup = BeautifulSoup(recipe_response.content, 'html.parser')

                plus = soup.find('img', alt_ ='Chefkoch Plus Logo')
                if plus:
                    continue

                recipe_dict = {}

                title = soup.find('h1').text
                recipe_dict['Title'] = title
                recipe_dict['URL'] = url
                prep_time = soup.find('span',class_='recipe-preptime rds-recipe-meta__badge')
                if prep_time:
                    icon = prep_time.find('i')
                    if icon:
                        icon.extract()
                    prep_time = prep_time.text.strip()
                    recipe_dict['Preparation time'] = prep_time


                calories = soup.find('span',class_='recipe-kcalories rds-recipe-meta__badge')
                if calories:
                    icon = calories.find('i')
                    if icon:
                        icon.extract()
                    calories = calories.text.strip()
                    recipe_dict['Calories'] = calories



                description_title = soup.find('h2',{'data-vars-tracking-title': 'Zubereitung'})
                if description_title:
                    description = description_title.find_next_sibling('div').text
                    recipe_dict['Description'] =description


                portions = soup.find('input', {'aria-label': 'Anzahl der Portionen'}).get('value')
                recipe_dict['Portions'] = portions


                image_div = soup.find('div', class_='recipe-image-carousel-slide')
                image_tag = image_div.find('img')
                image_srcset = image_tag['srcset'] if image_tag else None

                # Extract the first image URL from the srcset
                image_url = None
                if image_srcset:
                    image_url = image_srcset.split(',')[0].split(' ')[0]
                image_bytes = None
                if image_url:
                    image_response = requests.get(image_url)
                    image_bytes = image_response.content
                    recipe_dict['Image'] = base64.b64encode(image_bytes).decode('utf-8')
                    # Display the image
                    #image = Image.open(BytesIO(image_bytes))
                    #image.show()



                ingredients_tables = soup.find_all('table', class_='ingredients table-header')

                # List to hold all ingredients
                ingredients = []

                for table in ingredients_tables:
                    # Iterate over each row in the current ingredients table
                    for row in table.find_all('tr'):
                        # Extract the quantity and ingredient name from each row
                        quantity_td = row.find('td', class_='td-left')
                        ingredient_td = row.find('td', class_='td-right')
                        quantity = quantity_td.get_text(strip=True).replace(' ', '') if quantity_td else ''
                        ingredient = ingredient_td.get_text(strip=True) if ingredient_td else ''
                        ingredients.append(f"{quantity} - {ingredient}")

                recipe_dict['Ingredients'] = ingredients
                recipe_data_list.append(recipe_dict)
        else:
            print(f"Failed to retrieve content, status code: {response.status_code}")

    with open(f'../recipes_data/{meal}.json', 'w', encoding='utf-8') as f:
        json.dump(recipe_data_list, f, ensure_ascii=False, indent=4)
