from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class TeamRequest(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=3, max_length=3)
    pot: int = Field(..., ge=1, le=4)
    coefficient: float = Field(..., ge=0)
    logo_url: Optional[str] = None

    @validator('country')
    def country_uppercase(cls, v):
        return v.upper()

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Real Madrid",
                "country": "ESP",
                "pot": 1,
                "coefficient": 148.0,
                "logo_url": "https://example.com/real-madrid.png"
            }
        }


class DrawRequest(BaseModel):
    competition: str = Field(..., regex="^(champions_league|europa_league|conference_league)$")
    season: str = Field(..., regex="^\\d{4}/\\d{2}$")
    teams: List[TeamRequest] = Field(..., min_items=36, max_items=36)

    @validator('teams')
    def validate_pot_distribution(cls, teams):
        pot_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for team in teams:
            pot_counts[team.pot] += 1

        for pot, count in pot_counts.items():
            if count != 9:
                raise ValueError(f"Pot {pot} must contain exactly 9 teams, found {count}")

        return teams

    class Config:
        schema_extra = {
            "example": {
                "competition": "champions_league",
                "season": "2025/26",
                "teams": []
            }
        }


class ValidateDrawRequest(BaseModel):
    draw_id: int