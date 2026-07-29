from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    batting_team: str = Field(..., example="Chennai Super Kings")
    bowling_team: str = Field(..., example="Mumbai Indians")
    venue: str = Field(..., example="Wankhede Stadium, Mumbai")
    current_score: int = Field(..., ge=0, example=120)
    wickets_fallen: int = Field(..., ge=0, le=10, example=3)
    overs_completed: float = Field(..., ge=0.0, le=20.0, example=14.2)
    target_runs: int = Field(..., ge=1, example=175)
    toss_winner: Optional[str] = Field(None, example="Chennai Super Kings")
    toss_decision: Optional[str] = Field("field", example="field")

    @field_validator('bowling_team')
    def teams_must_be_different(cls, v, values):
        if 'batting_team' in values.data and v == values.data['batting_team']:
            raise ValueError('Batting team and Bowling team must be different.')
        return v


class PredictResponse(BaseModel):
    batting_team: str
    bowling_team: str
    chasing_team_win_prob: float
    defending_team_win_prob: float
    current_score: int
    wickets_fallen: int
    wickets_remaining: int
    overs_completed: float
    balls_left: int
    target_runs: int
    runs_left: int
    crr: float
    rrr: float
    phase: str
    h2h_win_pct: Optional[float] = 50.0
    projected_1st_innings: Optional[Dict[str, Any]] = None


class TeamInfo(BaseModel):
    name: str
    short_name: str
    primary_color: str
    secondary_color: str


class VenueInfo(BaseModel):
    name: str
    city: str


class MetadataResponse(BaseModel):
    teams: List[TeamInfo]
    venues: List[VenueInfo]
    default_venue: str
