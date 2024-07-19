import uvicorn
from fastapi import FastAPI
from common.client import connectDB

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
    client = connectDB()
