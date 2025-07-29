from pydantic import BaseModel


class GameWeekResponse(BaseModel):
    id: int
    name: str
    deadline_time: str

    class Config:
        extra = "ignore"