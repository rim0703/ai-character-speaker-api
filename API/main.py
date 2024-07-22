import uvicorn
from fastapi import FastAPI
from controller.device import router as DeviceRouter
from controller.voice import router as VoiceRouter

app = FastAPI()

app.include_router(DeviceRouter, tags=["Device"], prefix="/device")
app.include_router(VoiceRouter, tags=["Voice"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
