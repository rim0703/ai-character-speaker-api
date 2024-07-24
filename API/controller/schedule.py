from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from repository.voice import (
    find_scheduled_voice,
    create_schedule_voice,
    delete_schedule_voice,
    run_schedule,
)
from models.voice import Voice, CreateVoice, CreateScheduleVoice
from utils.hardwareService import sendVoiceToHardwareService
from common.response import Response
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
import tracemalloc
import pytz
import asyncio
from functools import partial

tracemalloc.start()


router = APIRouter()
# scheduler = BackgroundScheduler(timezone="Asia/Seoul", daemon=True)
# scheduler = BackgroundScheduler(daemon=True)
scheduler = AsyncIOScheduler()
# asyncio.get_event_loop().run_forever()


@router.get("")
async def get_schedule_list():
    schedule = await find_scheduled_voice()
    if schedule:
        return Response(schedule, "success")
    return Response(schedule, "empty")


async def run_async_function(voice):
    print(voice)
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    # loop.run_until_complete(create_schedule_job(voice=voice))
    # loop.close()

    await loop.run_in_executor(None, create_schedule_job, voice)


async def create_schedule_job(voice):
    print(voice)
    result = await run_schedule(voice)
    return "OK"


@router.post("")
async def create_schedule(voice: CreateScheduleVoice = Body(...)):
    global scheduler
    new_voice = await create_schedule_voice(jsonable_encoder(voice))
    timestamp = int(new_voice["schedule"]["timestamp"])

    timezone = pytz.timezone("Asia/Seoul")
    naive_datetime = datetime.fromtimestamp(timestamp)
    run_date = timezone.localize(naive_datetime)

    print(run_date)
    print(datetime.now())
    scheduler.print_jobs()

    if not scheduler.running:
        scheduler.start()
        print("Scheduler started")

    try:
        scheduler.add_job(
            create_schedule_job,
            trigger=DateTrigger(run_date=run_date, timezone=timezone),
            id=new_voice["voice_id"],
            args=[new_voice],
            misfire_grace_time=None,
        )

    except ValueError as e:
        print(f"Error adding job: {e}")

    scheduler.print_jobs()

    return Response(new_voice, "success")


async def remove_schedule_job(id):
    global scheduler
    if scheduler is not None:
        try:
            scheduler.remove_job(id)
        except:
            print("No Job ID")
        return "schedule removed"
    return "no schedule"


@router.delete("/{id}")
async def delete_schedule(id: str):
    t_schedule = await delete_schedule_voice(id)
    removed = await remove_schedule_job(id)
    result = {"action": t_schedule, "result": removed}
    return Response(result, "success")
