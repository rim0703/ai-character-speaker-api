from pydantic import BaseModel, Field


class Voice(BaseModel):
    voice_id: str = Field(...)
    character: str = Field(...)
    text: str = Field(...)

    class Config:
        schema_extra = {
            "voice_id": "1",
            "character": "짱구",
            "text": "밥먹을시간",
        }


class CreateVoice(BaseModel):
    character: str = Field(...)
    text: str = Field(...)

    class Config:
        schema_extra = {
            "character": "짱구",
            "text": "밥먹을시간이야",
        }
