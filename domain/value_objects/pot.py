from dataclasses import dataclass


@dataclass(frozen=True)
class Pot:
    """Value object representing a draw pot"""
    number: int

    def __post_init__(self):
        if not 1 <= self.number <= 4:
            raise ValueError("Pot number must be between 1 and 4")

    @property
    def name(self) -> str:
        return f"Pot {self.number}"

    def __str__(self):
        return self.name