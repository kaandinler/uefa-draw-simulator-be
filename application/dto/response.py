from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class TeamResponse(BaseModel):
    id: int
    name: str
    country: str
    pot: int
    coefficient: float
    logo_url: Optional[str] = None

    class Config:
        orm_mode = True


class FixtureResponse(BaseModel):
    opponent_id: int
    opponent_name: str
    opponent_country: str
    is_home: bool
    matchday: Optional[int] = None
    scheduled_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class TeamDrawResult(BaseModel):
    team: TeamResponse
    fixtures: List[FixtureResponse]
    home_games_count: int
    away_games_count: int


class DrawResponse(BaseModel):
    id: Optional[int]
    competition: str
    season: str
    results: List[TeamDrawResult]
    total_fixtures: int
    created_at: datetime
    is_valid: bool
    validation_errors: List[str] = []

    class Config:
        orm_mode = True


class ValidationResponse(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    statistics: Dict[str, Any]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
