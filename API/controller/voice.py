from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from repository.voice import create_voice, find_all_voices
from models.voice import Voice, CreateVoice
from utils.hardwareService import sendVoiceToHardwareService
from common.response import Response, ErrorResponse

router = APIRouter()


@router.post("/voice", response_description="Create New Voice")
async def create_new_voice(voice: CreateVoice = Body(...)):
    voice = jsonable_encoder(voice)
    new_voice = await create_voice(voice)
    return Response(new_voice, "success")


@router.get("/history", response_description="Get History")
async def get_voices_history():
    voices = await find_all_voices()
    if voices:
        return Response(voices, "success")
    return Response(voices, "empty")
