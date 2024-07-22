from fastapi import APIRouter, Body

from repository.voice import find_favorite_voices, update_favorite_voice
from common.response import Response

router = APIRouter()


@router.get("/")
async def get_favorite_list():
    favorites = await find_favorite_voices()
    if favorites:
        return Response(favorites, "success")
    return Response(favorites, "empty")


@router.put("/{id}")
async def change_favorite_status(id: str):
    favorite = await update_favorite_voice(id)
    return Response(favorite, "success")
