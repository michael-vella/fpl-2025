from pydantic import BaseModel


class PlayerResponse(BaseModel):
    id: int
    code: int
    first_name: str
    second_name: str
    element_type: int
    now_cost: int
    team: int
    expected_goals_per_90: float
    expected_assists_per_90: float
    expected_goal_involvements_per_90: float
    expected_goals_conceded_per_90: float

    class Config:
        extra = "ignore"