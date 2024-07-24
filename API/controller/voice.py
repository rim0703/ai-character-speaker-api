from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from repository.voice import create_voice, find_all_voices
from models.voice import CreateVoice
from utils.hardwareService import sendVoiceToHardwareService
from common.response import Response
import os


router = APIRouter()


@router.get("/voice/{id}", response_description="Get Voice File")
async def get_voice_file(id: str):
    system_path = "C:/Users/User/inference/"
    voice_store = "vitsoutput"
    file_name = id + ".wav"
    voice_path = os.path.join(system_path, voice_store, file_name)
    await sendVoiceToHardwareService(voice_path, file_name)
    return FileResponse(voice_path)


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
