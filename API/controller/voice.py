from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from repository.voice import create_voice
from models.voice import Voice, CreateVoice
from utils.hardwareService import sendVoiceToHardwareService
from common.response import Response, ErrorResponse

router = APIRouter()


@router.post("/", response_description="Create New Voice")
async def create_normal_voice(voice: CreateVoice = Body(...)):
    voice = jsonable_encoder(voice)
    new_voice = await create_voice(voice)
    return Response(new_voice, "soccess")
