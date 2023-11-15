## Setting Up the Virtual Environment

### Prerequisites
- Python 3.x
- Pip (Python package manager)

### Steps
1. **Create a Virtual Environment**: Navigate to the project directory and create a virtual environment named `venv`:

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**: With the virtual environment activated, install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the project root directory with the following content:

```
dbname=recipes
user=root
password=root
host=localhost
port=5432
```

These variables are used for database connections and should be kept secure.

## Running the Scraper

The `scraper.py` script is used to scrape data and store it in JSON format.

1. Run the scraper:
   ```bash
   python scraper.py
   ```

2. The script will output JSON files with the scraped data.

## Running the Database Pipeline

The `database_pipeline.py` script is responsible for downloading the scraped JSONs from Google Drive (avoiding storage on Git due to size constraints) and transforming the JSON into database tables.

### Steps

1. **Download JSON Files**: Run `database_pipeline.py`. It will download the JSON files from Google Drive into the `recipes_data` folder.

2. **Data Transformation and Database Insertion**:
   - The script creates three tables: `ingredients`, `recipes`, and a many-to-many relationship table for recipes and ingredients.
   - The script reads the JSON files, processes the data, and populates the tables.

3. Run the script:
   ```bash
   python database_pipeline.py
   ```

## Important Notes

- Ensure the virtual environment is activated (`venv`) when running scripts.
- The database credentials in the `.env` file should be valid and correspond to your database setup.
- The `requirements.txt` file contains all the necessary Python packages. Make sure they are installed in your virtual environment.
- The `config.json` file should be properly set with the Google Drive file IDs for the `database_pipeline.py` script to function correctly.
