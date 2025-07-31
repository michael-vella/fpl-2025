from pydantic import BaseModel


class PlayerTypeResponse(BaseModel):
    id: int
    singular_name_short: str
    squad_select: int

    class Config:
        extra = "ignore"