from pydantic import BaseModel


class FixtureResponse(BaseModel):
    code: int

    class Config:
        extra = "ignore"