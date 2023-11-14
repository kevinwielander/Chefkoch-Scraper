import psycopg2
from PIL import Image
from io import BytesIO

# Replace these with your database connection details
dbname = "recipes"
user = "root"
password = "root"
host = "localhost"
port = "5432"

# Replace this with the entry ID you want to retrieve
entry_id_to_retrieve = 902

# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()

    # Retrieve the entry with the specified ID
    retrieve_query = "SELECT title, image FROM recipes WHERE id = %s;"
    cursor.execute(retrieve_query, (entry_id_to_retrieve,))
    entry = cursor.fetchone()

    if entry:
        name, image_data = entry

        # Display the name and steps
        print(f"Name: {name}")
        print(f"image_data: {str(image_data)}")

        # Display the image
        if image_data:
            image = Image.open(BytesIO(image_data))
            image.show()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
