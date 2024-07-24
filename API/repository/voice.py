from common.client import connectDB
from bson.objectid import ObjectId
from fastapi.responses import FileResponse
from models.favorite import Favorite
from typing import Union

from utils.hardwareService import sendVoiceToHardwareService
import time
import subprocess
import os


def voice_helper(voice) -> dict:
    return {
        "voice_id": str(voice["_id"]),
        "character": str(voice["character"]),
        "content": str(voice["content"]),
        "file_path": str(voice["file_path"]),
        "created_at": str(voice["created_at"]),
        "updated_at": str(voice["updated_at"]),
        "favorite": dict(voice["favorite"]),
        "schedule": dict(voice["schedule"]),
        "status": str(voice["status"]),
    }


def voice_repository():
    db = connectDB()
    voice = db.get_collection("voice")
    return voice


def voice_generator(character, content, idx):
    origin_path = os.getcwd()
    system_path = "C:/Users/User/inference/"
    voice_store = "vitsoutput"
    conda_env_name = "tts_infer"
    cpu_script_path = "voice_service.py"
    os.chdir(system_path)

    command = f'conda run -n {conda_env_name} python {cpu_script_path} {character} "{" "+content+" ~"}" {idx}'

    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            file_name = idx + ".wav"
            voice_path = os.path.join(system_path, voice_store, file_name)
            os.chdir(origin_path)
            print("stdout:", result.stdout)
            return voice_path, file_name
        else:
            print("stderr:", result.stderr)
            return result.stderr

    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)


async def create_voice(new_voice):
    voice = voice_repository()
    new_voice["created_at"] = int(time.time())
    new_voice["updated_at"] = int(time.time())
    new_voice["favorite"] = {"name": "", "like": False}
    new_voice["status"] = ""
    new_voice["file_path"] = ""
    new_voice["schedule"] = {"timestamp": 0}
    new_voice = await voice.insert_one(new_voice)
    new_voice = await voice.find_one({"_id": new_voice.inserted_id})

    result = voice_generator(
        new_voice["character"], new_voice["content"], str(new_voice["_id"])
    )
    result = await sendVoiceToHardwareService(result[0], result[1])
    new_voice["status"] = result["status"]

    return voice_helper(new_voice)


async def find_all_voices():
    voice = voice_repository()
    voice_list = []
    current_time = int(time.time())
    async for v in voice.find():
        if int(v["schedule"]["timestamp"]) < current_time:
            voice_list.append(voice_helper(v))
    voice_list = sorted(voice_list, key=lambda x: x["created_at"], reverse=True)
    return voice_list


async def find_favorite_voices():
    voice = voice_repository()
    voice_list = []
    async for v in voice.find():
        if v["favorite"]["like"]:
            voice_list.append(voice_helper(v))
    voice_list = sorted(voice_list, key=lambda x: x["updated_at"], reverse=True)
    return voice_list


async def update_favorite_voice(id, info):
    voice = voice_repository()
    voice_one = await voice.find_one({"_id": ObjectId(id)})
    if bool(voice_one["favorite"]["like"]):
        voice_one["favorite"]["like"] = False
        voice_one["favorite"]["name"] = ""
    else:
        voice_one["favorite"]["like"] = True
        voice_one["favorite"]["name"] = info["name"]
    voice.update_one({"_id": ObjectId(id)}, {"$set": voice_one})
    return voice_helper(voice_one)


async def find_scheduled_voice():
    voice = voice_repository()
    voice_list = []
    current_time = int(time.time())
    async for v in voice.find():
        if int(v["schedule"]["timestamp"]) > current_time:
            voice_list.append(voice_helper(v))
    return voice_list


async def create_schedule_voice(new_voice):
    voice = voice_repository()
    new_voice["created_at"] = int(time.time())
    new_voice["updated_at"] = new_voice["schedule"]["timestamp"]
    new_voice["favorite"] = {"name": "", "like": False}
    new_voice["status"] = ""
    new_voice["file_path"] = ""
    new_voice = await voice.insert_one(new_voice)
    new_voice = await voice.find_one({"_id": new_voice.inserted_id})
    return voice_helper(new_voice)


async def run_schedule(new_voice):
    result = voice_generator(
        new_voice["character"], new_voice["content"], str(new_voice["voice_id"])
    )
    result = await sendVoiceToHardwareService(result[0], result[1])
    return "OK"


async def delete_schedule_voice(id):
    voice = voice_repository()
    old_voice = await voice.delete_one({"_id": ObjectId(id)})
    print(old_voice)
    return "deleted"
