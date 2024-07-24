from pydantic import BaseModel, Field
from typing import Optional


class Favorite(BaseModel):
    name: str = ""
    like: bool = False


class CreateFavorite(BaseModel):
    name: str = Field(...)


class UpdateFavorite(BaseModel):
    voice_id: str = Field(...)
