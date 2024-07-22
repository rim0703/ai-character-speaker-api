from pydantic import BaseModel, Field
from typing import Union
import time
from models.favorite import Favorite
from models.schedule import Schedule


class Voice(BaseModel):
    character: str = Field(...)
    text: str = Field(...)
    file_path: str = ""
    created_at: str = str(int(time.time()))
    favorite: Union[Favorite, None] = None
    schedule: Union[Schedule, None] = None
    status: str = ""


class CreateVoice(BaseModel):
    character: str = Field(...)
    text: str = Field(...)
    file_path: str = ""
    created_at: str = str(int(time.time()))
    favorite: Union[Favorite, None] = None
    schedule: Union[Schedule, None] = None
    status: str = ""
