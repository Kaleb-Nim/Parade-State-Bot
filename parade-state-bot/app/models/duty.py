"""Models for duty instructor (DI) management."""
from datetime import date
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DutyInstructor(BaseModel):
    """Model representing a duty instructor."""

    name: str
    rank: str
    duty_date: date

    def __str__(self) -> str:
        """String representation of DI."""
        return f"{self.rank} {self.name}"


class DutySchedule(BaseModel):
    """Collection of duty instructor schedules."""

    schedule: Dict[date, DutyInstructor] = Field(default_factory=dict)

    def get_di_for_date(self, target_date: date) -> Optional[DutyInstructor]:
        """Get the duty instructor for a specific date.

        Args:
            target_date: The date to look up

        Returns:
            DutyInstructor if found, None otherwise
        """
        return self.schedule.get(target_date)

    def get_next_di(self, from_date: date) -> Optional[DutyInstructor]:
        """Get the next duty instructor after a given date.

        Args:
            from_date: Starting date

        Returns:
            Next DutyInstructor if found, None otherwise
        """
        # Get all dates that are after from_date
        future_dates = [d for d in self.schedule.keys() if d > from_date]
        if not future_dates:
            return None

        # Get the closest future date
        next_date = min(future_dates)
        return self.schedule.get(next_date)