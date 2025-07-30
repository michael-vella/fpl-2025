from pydantic import BaseModel


class TeamResponse(BaseModel):
    id: int
    code: int
    name: str
    short_name: str
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int

    class Config:
        extra = "ignore"