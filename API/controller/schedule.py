from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from repository.voice import (
    find_scheduled_voice,
    create_schedule_voice,
    delete_schedule_voice,
)
from models.voice import Voice, CreateVoice
from utils.hardwareService import sendVoiceToHardwareService
from common.response import Response
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from apscheduler.triggers.date import DateTrigger

router = APIRouter()
scheduler = BackgroundScheduler(timezone="Asia/Seoul", daemon=True)


@router.get("/")
async def get_schedule_list():
    schedule = await find_scheduled_voice()
    if schedule:
        return Response(schedule, "success")
    return Response(schedule, "empty")


@router.post("/")
async def create_schedule(voice: CreateVoice = Body(...)):
    new_voice = await create_schedule_voice(jsonable_encoder(voice))

    timestamp = int(new_voice["schedule"]["timestamp"])
    run_date = datetime.fromtimestamp(timestamp)
    try:
        scheduler.add_job(
            create_schedule_job,
            run_date=run_date,
            id=new_voice["voice_id"],
            args=[new_voice],
        )
    except ValueError as e:
        print(f"Error adding job: {e}")

    if not scheduler.running:
        scheduler.start()

    return Response(new_voice, "success")


def create_schedule_job(voice):
    # TODO: schedule + speaker

    return "OK"


async def remove_schedule_job(id):
    global scheduler
    if scheduler is not None:
        scheduler.remove_job(id)
        return "schedule removed"
    return "no schedule"


@router.delete("/{id}")
async def delete_schedule(id: str):
    t_schedule = await delete_schedule_voice(id)
    removed = await remove_schedule_job(id)
    result = {"action": t_schedule, "result": removed}
    return Response(result, "success")
