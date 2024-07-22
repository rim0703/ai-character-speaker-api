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

router = APIRouter()


@router.get("/")
async def get_schedule_list():
    schedule = await find_scheduled_voice()
    if schedule:
        return Response(schedule, "success")
    return Response(schedule, "empty")


@router.post("/")
async def create_schedule(voice: CreateVoice = Body(...)):
    voice = jsonable_encoder(voice)
    new_voice = await create_schedule_voice(voice)
    # TODO: schedule + speaker

    return Response(new_voice, "success")


@router.delete("/{id}")
async def delete_schedule(id: str):
    t_schedule = await delete_schedule_voice(id)
    return Response(t_schedule, "success")
