import requests
from bs4 import BeautifulSoup

# Function to extract options from a dropdown list
def extract_dropdown_options(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    select_elements = soup.find_all('select')
    return select_elements
    # Extract the text of each option element
    #options = [option.text.strip() for option in option_elements]

    #return options

# URL of the webpage to fetch
url = 'https://www.chefkoch.de/rezepteingabe/wizard/'

# Make a GET request to fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Extract the options from the dropdown list
    options = extract_dropdown_options(response.text)

    # Print the extracted options
    for option in options:
        print(option)
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
