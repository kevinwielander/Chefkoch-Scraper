import scrapy

# Base URL
base_url = 'https://www.chefkoch.de/'

# Paths for different meal types
meal_paths = {
    'breakfast': 'rs/s0t53/Fruehstueck-Rezepte.html',
    # 'snack': 'rs/s0t71/Snack-Rezepte.html',
    # 'dessert': 'rs/s0t90/Dessert-Rezepte.html',
    # 'side_dish': 'rs/s0t36/Beilage-Rezepte.html',
    # 'starter': 'rs/s0t19/Vorspeise-Rezepte.html',
    # 'main_dish': 'rs/s0t21/Hauptspeise-Rezepte.html'
}

# Add the base URL to each path
full_urls = {meal: base_url + path for meal, path in meal_paths.items()}

for url in full_urls.values():
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        recipe_links = [link['href'] for link in soup.find_all('a', class_='ds-recipe-card__link ds-teaser-link')]
        print(recipe_links)

        for link in recipe_links:
            recipe_response = requests.get(link)
            soup = BeautifulSoup(recipe_response.content, 'html.parser')
            title = soup.find('h1').text
            prep_time = soup.find('span',class_='recipe-preptime rds-recipe-meta__badge')
            if prep_time:
                icon = prep_time.find('i')
                if icon:
                    icon.extract()
                prep_time = prep_time.text.strip()
            calories = soup.find('span',class_='recipe-kcalories rds-recipe-meta__badge')
            if calories:
                icon = calories.find('i')
                if icon:
                    icon.extract()
                calories = calories.text.strip()
            description_title = soup.find('h2',{'data-vars-tracking-title': 'Zubereitung'})
            if description_title:
                description = description_title.find_next_sibling('div').text

            portions = soup.find('input', {'aria-label': 'Anzahl der Portionen'}).get('value')

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
                # Display the image
                #image = Image.open(BytesIO(image_bytes))
                #image.show()


            print(f"Title: {title}, Prep Time: {prep_time}, Portions: {portions}, Calories: {calories}, Description: {description}")

            ingredients_table = soup.find('table', class_='ingredients table-header')

            # List to hold all ingredients
            ingredients = []

            # Iterate over each row in the ingredients table
            for row in ingredients_table.find_all('tr'):
                # Extract the quantity and ingredient name from each row
                quantity = row.find('td', class_='td-left').text.replace(" ","")
                ingredient = row.find('td', class_='td-right').text.strip()

                # Add the ingredient to the list
                ingredients.append(f"{quantity} - {ingredient}")

            # Print the ingredients
            for ingredient in ingredients:
                print(ingredient)
            print('--------')
    else:
        print(f"Failed to retrieve content, status code: {response.status_code}")


