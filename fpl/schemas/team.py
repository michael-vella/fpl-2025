from pydantic import BaseModel


class TeamResponse(BaseModel):
    id: int
    code: int
    name: str
    short_name: str

    class Config:
        extra = "ignore"