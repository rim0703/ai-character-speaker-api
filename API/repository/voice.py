from common.client import connectDB


def voice_helper(voice) -> dict:
    return {
        "voice_id": str(voice["_id"]),
        "character": str(voice["character"]),
        "text": str(voice["text"]),
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
