from pydantic import BaseModel


class PlayerResponse(BaseModel):
    code: int
    first_name: str

    class Config:
        extra = "ignore"