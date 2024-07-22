import motor.motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)


def connectDB():
    db_name = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    MONGO_DETAILS = "mongodb://" + str(db_name) + ":" + str(db_port)
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    return client.speaker
