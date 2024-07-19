from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


def connectDB():
    db_name = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    client = MongoClient(host=db_name, port=int(db_port))
    return client
