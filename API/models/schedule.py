from pydantic import BaseModel


class Schedule(BaseModel):
    timestamp: int
