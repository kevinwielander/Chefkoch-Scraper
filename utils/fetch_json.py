import requests


def get_file_from_google_drive(file_name, drive_link):
    file_id = drive_link.split('/')[-2]
    download_url = drive_link

    response = requests.get(download_url)
    print(response.json())
    if response.status_code == 200:
        with open(file_name, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(response.content)
    else:
        raise Exception(f"Error fetching file: {response.status_code}")



