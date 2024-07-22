from common.client import connectDB


def voice_helper(voice) -> dict:
    return {
        "voice_id": str(voice["_id"]),
        "character": str(voice["character"]),
        "text": str(voice["text"]),
        "file_path": str(voice["file_path"]),
        "created_at": str(voice["created_at"]),
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
