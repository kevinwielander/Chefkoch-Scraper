import gdown
import requests
import os
import json

# Folder to save the files
output_folder = '../recipes_data'


def download_file_from_google_drive(file_id, destination):
    """Download a file from Google Drive using its ID."""
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)
    print(f"Downloaded {destination}")


def get_confirm_token(response):
    """Get the confirmation token to download large files."""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    """Save the content of the response to a file."""
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def download_and_save_recipes():
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read config file
    with open('utils/config.json', 'r') as file:
        config = json.load(file)

    # Process each file
    for file_info in config['files']:
        file_path = os.path.join(output_folder, file_info['name'] + '.json')
        download_file_from_google_drive(file_info['id'], file_path)


