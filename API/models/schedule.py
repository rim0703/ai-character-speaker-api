from pydantic import BaseModel


class Schedule(BaseModel):
    date: str = ""
    time: str = ""
