from pydantic import BaseModel, Field


class Favorite(BaseModel):
    name: str = ""
    like: bool = False
