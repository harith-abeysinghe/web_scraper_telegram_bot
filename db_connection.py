import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_mongo_uri():
    # MongoDB Configuration
    db_password = os.getenv("DB_PASSWORD")  # Load the password from environment variables
    if not db_password:
        raise ValueError("Environment variable 'DB_PASSWORD' is not set.")

    # Escape the password to handle special characters
    escaped_password = quote_plus(db_password)

    # MongoDB URI with escaped password
    uri = f"mongodb+srv://harithabeysinghe:{escaped_password}@cryptonewsscrpaer.omp2w.mongodb.net/?retryWrites=true&w=majority&appName=CryptoNewsScraper"

    return uri


def connect_to_mongodb():
    uri = get_mongo_uri()
    try:
        client = MongoClient(uri)
        db = client["Crypto"]  # Specify your database name
        collection = db["CryptoNews"]  # Specify your collection name
        print("Successfully connected to MongoDB!")
        return collection
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {e}")
