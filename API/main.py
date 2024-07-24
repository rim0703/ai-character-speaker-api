import uvicorn
import asyncio
from fastapi import FastAPI, Body
from controller.device import router as DeviceRouter
from controller.voice import router as VoiceRouter
from controller.favorite import router as FavoriteRouter
from controller.schedule import router as ScheduleRouter
from controller.schedule import create_schedule
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from controller.schedule import scheduler

origins = ["http://localhost:3000"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(DeviceRouter, tags=["Device"], prefix="/device")
app.include_router(VoiceRouter, tags=["Voice"])
app.include_router(ScheduleRouter, tags=["Schedule"], prefix="/schedule")
app.include_router(FavoriteRouter, tags=["Favorites"], prefix="/favorites")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
