from datetime import datetime

from pydantic import BaseModel


class GameweekResponse(BaseModel):
    id: int
    name: str
    deadline_time: datetime

    class Config:
        extra = "ignore"