import pandas as pd
from pymongo import MongoClient, errors
import logging
import os
from datetime import datetime
import configparser

# Read config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get values from config
mongo_uri = config.get('database', 'mongo_uri')
db_name = config.get('database', 'db_name')
collection_name = config.get('database', 'collection_name')
csv_file = config.get('files', 'csv_file')
log_dir = config.get('files', 'log_dir')
log_level = config.get('logging', 'log_level', fallback='INFO').upper()

# Setup logging
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"weather_loader_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    filename=log_file,
    level=getattr(logging, log_level),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_csv_to_mongo():
    try:
        # MongoDB connection
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]
        logging.info("Connected to MongoDB successfully.")

        # Read CSV
        try:
            df = pd.read_csv(csv_file, encoding='latin1')
            logging.info(f"Successfully read CSV file: {csv_file}")
        except FileNotFoundError:
            logging.error(f"CSV file '{csv_file}' not found.")
            return
        except pd.errors.ParserError as e:
            logging.error(f"Parsing error while reading the CSV: {e}")
            return

        # Convert to records
        records = df.to_dict(orient='records')
        if not records:
            logging.warning("CSV file is empty. No records to insert.")
            return

        # Clear existing data
        collection.delete_many({})
        logging.info("Cleared existing records from the collection.")

        # Insert new data
        collection.insert_many(records)
        logging.info(f"Inserted {len(records)} records into MongoDB collection '{collection_name}'.")

    except errors.ConnectionFailure as e:
        logging.error(f"MongoDB connection failed: {e}")
    except errors.PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    load_csv_to_mongo()
