from datetime import datetime

from pydantic import BaseModel


class FixtureResponse(BaseModel):
    id: int
    code: int
    event: int
    kickoff_time: datetime
    team_a: int
    team_h: int

    class Config:
        extra = "ignore"