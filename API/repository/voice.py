from common.client import connectDB
from bson.objectid import ObjectId
import time


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


async def create_voice(new_voice):
    voice = voice_repository()
    new_voice = await voice.insert_one(new_voice)
    new_voice = await voice.find_one({"_id": new_voice.inserted_id})

    # TODO: connect to hardware

    # TODO: play the voice

    return voice_helper(new_voice)


async def find_all_voices():
    voice = voice_repository()
    voice_list = []
    async for v in voice.find():
        voice_list.append(voice_helper(v))
    return voice_list


async def find_favorite_voices():
    voice = voice_repository()
    voice_list = []
    async for v in voice.find():
        if v["favorite"]["like"]:
            voice_list.append(voice_helper(v))
    return voice_list


async def update_favorite_voice(id):
    voice = voice_repository()
    voice_one = await voice.find_one({"_id": ObjectId(id)})
    if bool(voice_one["favorite"]["like"]):
        voice_one["favorite"]["like"] = False
    else:
        voice_one["favorite"]["like"] = True
    voice_one["updated_at"] = str(int(time.time()))
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
    new_voice = await voice.insert_one(new_voice)
    new_voice = await voice.find_one({"_id": new_voice.inserted_id})

    # TODO: connect to hardware

    # TODO: play the voice

    return voice_helper(new_voice)


async def delete_schedule_voice(id):
    voice = voice_repository()
    old_voice = await voice.delete_one({"_id": ObjectId(id)})
    print(old_voice)
    return "deleted"
