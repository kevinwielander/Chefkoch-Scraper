import base64

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image
from io import BytesIO
import json

# author: Cveta, Kevin
# TU Wien, 2023

chrome_options = Options()
chrome_options.add_argument("--headless")

# Base URL
base_url = 'https://www.chefkoch.de/'
max_page = 23
# Paths for different meal types
meal_paths = {
    'breakfast': 'rs/s$page$t53/Fruehstueck-Rezepte.html',
    'snack': 'rs/s$page$t71/Snack-Rezepte.html',
    'dessert': 'rs/s$page$t90/Dessert-Rezepte.html',
    'side_dish': 'rs/s$page$t36/Beilage-Rezepte.html',
    'starter': 'rs/s$page$t19/Vorspeise-Rezepte.html',
    'main_dish': 'rs/s$page$t21/Hauptspeise-Rezepte.html'
}

# Add the base URL to each path
full_urls = {meal: base_url + path for meal, path in meal_paths.items()}

driver = webdriver.Chrome(options=chrome_options)

driver.implicitly_wait(1)

# Function to accept cookies
def accept_cookies(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Zustimmen"]'))
        )
        # Click the accept button
        driver.find_element(By.CSS_SELECTOR, 'button[title="Zustimmen"]').click()
    except TimeoutException:
        # No cookie pop-up found or took too long to load
        pass


for meal, url in full_urls.items():
    recipe_data_list = []
    for i in range(max_page):
        url_current = url.replace('$page$', str(i))
        driver.get(url_current)
        print("Current Page:"+str(i))
        accept_cookies(driver)
        # Wait for the page to load
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ds-recipe-card__link"))
        )

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        recipe_links = [link['href'] for link in soup.find_all('a', class_='ds-recipe-card__link ds-teaser-link')]

        for link in recipe_links:
            try:
                print(link)
                driver.get(link)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                plus = soup.find('img', alt_='Chefkoch Plus Logo')
                if plus:
                    continue

                recipe_dict = {}

                # Retrieve the title
                title = driver.find_element(By.TAG_NAME, 'h1').text
                recipe_dict['Title'] = title
                recipe_dict['URL'] = url_current

                # Retrieve the preparation time
                prep_time_elements = driver.find_elements(By.CLASS_NAME, 'recipe-preptime.rds-recipe-meta__badge')
                prep_time = prep_time_elements[0].text.strip() if prep_time_elements else None
                recipe_dict['Preparation time'] = prep_time

                # Retrieve the calories
                calories_elements = driver.find_elements(By.CLASS_NAME, 'recipe-kcalories.rds-recipe-meta__badge')
                calories = calories_elements[0].text.strip() if calories_elements else None
                recipe_dict['Calories'] = calories

                # Retrieve the description
                description_elements = driver.find_elements(By.XPATH, '//h2[@data-vars-tracking-title="Zubereitung"]')
                description = description_elements[0].find_element(By.XPATH,
                                                                   'following-sibling::div').text if description_elements else None
                recipe_dict['Description'] = description

                # Retrieve the portions
                portions_element = driver.find_element(By.XPATH, '//input[@aria-label="Anzahl der Portionen"]')
                portions = portions_element.get_attribute('value') if portions_element else None
                recipe_dict['Portions'] = portions

                # Retrieve the image
                image_elements = driver.find_elements(By.CLASS_NAME, 'recipe-image-carousel-slide')
                if image_elements:
                    image_tag = image_elements[0].find_element(By.TAG_NAME, 'img')
                    image_srcset = image_tag.get_attribute('srcset')
                    image_url = image_srcset.split(',')[0].split(' ')[0] if image_srcset else None
                    if image_url:
                        image_bytes = requests.get(image_url).content
                        recipe_dict['Image'] = base64.b64encode(image_bytes).decode('utf-8')

                # Retrieve the ingredients
                ingredients = []
                ingredients_tables = driver.find_elements(By.CLASS_NAME, 'ingredients.table-header')
                for table in ingredients_tables:
                    rows = table.find_elements(By.TAG_NAME, 'tr')
                    for row in rows:
                        quantity_tds = row.find_elements(By.CLASS_NAME, 'td-left')
                        ingredient_tds = row.find_elements(By.CLASS_NAME, 'td-right')
                        quantity = quantity_tds[0].text.strip().replace(' ', '') if quantity_tds else ''
                        ingredient = ingredient_tds[0].text.strip() if ingredient_tds else ''

                        # Skip the ingredient if both amount and ingredient are empty
                        if not quantity and not ingredient:
                            continue

                        ingredient_dict = {
                            'amount': quantity,
                            'ingredient': ingredient
                        }
                        ingredients.append(ingredient_dict)

                recipe_dict['Ingredients'] = ingredients
                recipe_data_list.append(recipe_dict)
            except Exception as e:
                print(f"An error occurred while processing the recipe at {link}: {e}")

        with open(f'../recipes_data/{meal}_page_{i}.json', 'w', encoding='utf-8') as f:
            json.dump(recipe_data_list, f, ensure_ascii=False, indent=4)
