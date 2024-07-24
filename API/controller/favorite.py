from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from repository.voice import find_favorite_voices, update_favorite_voice
from common.response import Response
from models.favorite import CreateFavorite

router = APIRouter()


@router.get("")
async def get_favorite_list():
    favorites = await find_favorite_voices()
    if favorites:
        return Response(favorites, "success")
    return Response(favorites, "empty")


@router.put("/{id}")
async def create_favorite(id, favorite: CreateFavorite = Body(...)):
    favorite = await update_favorite_voice(id, jsonable_encoder(favorite))
    return Response(favorite, "success")


# @router.delete("")
# async def delete_favorite(favorite: UpdateFavorite = Body(...)):
#     favorite = await delete_favorite_voice(jsonable_encoder(favorite))
#     return Response(favorite, "success")
