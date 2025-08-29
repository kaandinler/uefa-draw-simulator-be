from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Team:
    """Team entity representing a football team in the competition"""
    id: int
    name: str
    country: str
    pot: int
    coefficient: float
    logo_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("Team name cannot be empty")
        if self.pot not in range(1, 5):
            raise ValueError("Pot must be between 1 and 4")
        if self.coefficient < 0:
            raise ValueError("Coefficient cannot be negative")
        if len(self.country) != 3:
            raise ValueError("Country code must be 3 characters")

    def is_same_country(self, other: 'Team') -> bool:
        """Check if two teams are from the same country"""
        return self.country == other.country

    def __eq__(self, other):
        if not isinstance(other, Team):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)