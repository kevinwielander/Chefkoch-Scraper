import scrapy

# Base URL
base_url = 'https://www.chefkoch.de/'

# Paths for different meal types
meal_paths = {
    'breakfast': 'rs/s0t53/Fruehstueck-Rezepte.html',
    'snack': 'rs/s0t71/Snack-Rezepte.html',
    'dessert': 'rs/s0t90/Dessert-Rezepte.html',
    'side_dish': 'rs/s0t36/Beilage-Rezepte.html',
    'starter': 'rs/s0t19/Vorspeise-Rezepte.html',
    'main_dish': 'rs/s0t21/Hauptspeise-Rezepte.html'
}

# Add the base URL to each path
full_urls = {meal: base_url + path for meal, path in meal_paths.items()}

# chefkoch_spider.py
# run from project folder with console command:
# scrapy crawl chefkoch -o chefkoch.json
#
# author: Cveta, Kevin
# TU Wien, 2023


class ChefkochSpider(scrapy.Spider):
    name = "chefkoch"
    start_urls = full_urls

    def parse(self, response):
        '''
        This function opens the webpages that show all recipes page by page.
        For every recipe link on those pages, parse_recipe is being called,
        which extracts the detail information from each recipe page.
        The result will be stored into a .json file if the spider is run as described above.
        '''

        # Get all links on the page (returns approx. 30 links)
        links = response.css('li.search-list-item a').css('::attr(href)').extract()
        # Iterate list of links and for each run parse_recipe
        for x in range(len(links)):
            yield response.follow(''.join(links[x] + '#'), self.parse_recipe)
            x += 1

            # Go to next page as long as there is one
        ## 1. get url for the next page
        next_p = response.css('a.qa-pagination-next').css('::attr(href)').extract_first()
        ## 2. add identifier for expanded webpage
        next_p += '#more2'
        ## 3. if next_page exists, go there
        if next_p != []:
            yield response.follow(next_p, self.parse)

    def parse_recipe(self, response):
        # table contains the recipe statistics and the ingredients
        # first, we get all fields from that table and put them in a  list
        table = response.xpath('//*[@id="recipe-statistic"]/table').xpath('//td/text()').extract()
        # second, we remove unnecessary characters and empty list elements
        for x in range(len(table)):
            table[x] = table[x].replace('\xa0', ' ').replace('\n', '').replace(' ', '')
        table = list(filter(None, table))
        # third, we split up table to statistics (which is always the first 9 entries) and
        #   ingredients (which is the rest)
        statistics = table[0:9]
        ingredients = table[9:-1]

        # We can extract details about the user
        # this section provides us info about how active the user is and when he or she joined
        user_details = response.css('div.user-details').css('::text').extract()
        for x in range(len(user_details)):
            user_details[x] = user_details[x].replace('\n', '').replace('\t', '')
        user_details = list(filter(None, user_details))

        # Next, we extract the preparation meta data
        # The webpage contains info about preparation/cooking/resting time, difficulty and calories
        prep_info = response.xpath('//*[@id="preparation-info"]').css('::text').extract()
        for x in range(len(prep_info)):
            prep_info[x] = prep_info[x].replace('\n', '').replace(' ', '').replace('/', '')
        prep_info.pop(0)

        # Next, initialize variables that we want to extract from prep_info
        time_work = ''
        time_cook = ''
        time_rest = ''
        difficulty = ''
        calories = ''

        # Finally, iterate the prep_list to extract these variables
        # Not all recipes have all time values, which is why the iteration must be flexible
        for x in range(len(prep_info)):
            if prep_info[x] == 'Arbeitszeit:':
                time_work = prep_info[x + 1]
            if prep_info[x] == 'Koch-Backzeit:':
                time_cook = prep_info[x + 1]
            if prep_info[x] == 'Ruhezeit:':
                time_rest = prep_info[x + 1]
            if prep_info[x] == 'Schwierigkeitsgrad:':
                difficulty = prep_info[x + 1]
            if prep_info[x] == 'Kalorienp.P.:':
                calories = prep_info[x + 1]

        # We want to scrape the preparation steps as well
        preplist = response.css('div.instructions::text').extract()

        # this gives a list of Strings which has to be cleaned
        # We need to remove those elements
        preplist_filtered = ''
        for i in preplist:
            preplist_filtered += ''.join(i)
        preplist_filtered = preplist_filtered.replace('\n', '')
        preplist_filtered = preplist_filtered.replace('     ', '')

        yield {
            'name': response.css('h1.page-title::text').extract_first(),
            'subtitle': response.css('div.summary::text').extract_first(),
            'user': user_details[0],
            'user_date': user_details[2],
            'user_activity': user_details[3],
            'date': statistics[2],
            'number_ratings': statistics[0].replace('(', ''),
            'avg_rating': response.css('span.rating__average-rating::text').extract_first(),
            'saved': statistics[4],
            'printed': statistics[6],
            'shared': statistics[8],
            'time_work': time_work,
            'time_cook': time_cook,
            'time_rest': time_rest,
            'difficulty': difficulty,
            'calories': calories,
            'ingredients': ingredients,
            'preparation': preplist_filtered
        }
