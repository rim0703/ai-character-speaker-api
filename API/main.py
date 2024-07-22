import uvicorn
from fastapi import FastAPI
from controller.device import router as DeviceRouter

app = FastAPI()

app.include_router(DeviceRouter, tags=["Device"], prefix="/device")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
