"""Models for staff members and their status."""
from datetime import date
from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class StatusType(str, Enum):
    """Enumeration of possible staff status types."""

    PRESENT = "P"  # Present
    CSE = "CSE"  # Course
    CPE = "CPE"  # Course Preparation Exercise
    OL = "OL"  # Overseas Leave
    OML = "OML"  # Off Medical Leave
    LL = "LL"  # Local Leave
    HL = "HL"  # Hospitalization Leave
    WFH = "WFH"  # Work From Home
    MC = "MC"  # Medical Certificate
    OIL = "OIL"  # Off-In-Lieu
    DO = "DO"  # Day Off
    ACE = "ACE"  # Annual cohesion exercise
    FCL = "FCL"  # Family care leave
    MA = "MA"  # Medical Appointment
    RS = "RS"  # Regular Screening?
    OB = "OB"  # Out Bounds / Official Business
    AO = "AO"  # Attached Out
    OTH = "OTH"  # Other
    DS = "DS"  # DS Off / Duty Staff
    OTHERS = "OTHERS"  # Catch-all for unrecognized status


class StaffSynonym(BaseModel):
    """Dictionary representing a synonyms for a staff member. Used for lookup when not found."""

    name: str
    synonyms: List[str] = Field(default_factory=list)

    def __str__(self) -> str:
        """String representation of staff synonym."""
        return f"{self.name} ({', '.join(self.synonyms)})"


class LocationDetail(BaseModel):
    """Model representing a location or specific detail for a status."""

    location: Optional[str] = None
    detail: Optional[str] = None

    def __str__(self) -> str:
        """String representation of location detail."""
        if self.location and self.detail:
            return f"@ {self.location} ({self.detail})"
        elif self.location:
            return f"@ {self.location}"
        elif self.detail:
            return f"({self.detail})"
        return ""


class StaffStatus(BaseModel):
    """Model representing a staff member's status."""

    status_type: StatusType
    end_date: Optional[date] = None
    details: Optional[str] = None
    location: Optional[LocationDetail] = None
    am_pm_split: bool = False
    am_status: Optional[StatusType] = None
    am_location: Optional[LocationDetail] = None
    pm_status: Optional[StatusType] = None
    pm_location: Optional[LocationDetail] = None

    def format_status(self) -> str:
        """Format the status for display in the parade state message."""
        if not self.am_pm_split:
            # Simple status - no AM/PM split
            if self.status_type == StatusType.PRESENT:
                result = f"{self.status_type}"
                if self.details:
                    result += f" {self.details}"
                return result

            result = f"{self.status_type}"
            if self.location:
                result += f" {self.location}"
            if self.details:
                result += f" {self.details}"
            if self.end_date:
                result += f" TILL {self.end_date.strftime('%d/%m')}"
            return result

        # Handle AM/PM split
        am_part = f"{self.am_status or self.status_type}"
        if self.am_location:
            am_part += f" {self.am_location}"

        pm_part = f"{self.pm_status or self.status_type}"
        if self.pm_location:
            pm_part += f" {self.pm_location}"

        result = f"{am_part}(AM), {pm_part}(PM)"
        
        # Add end date if applicable
        if self.end_date:
            result += f" TILL {self.end_date.strftime('%d/%m')}"
            
        return result


class StaffMember(BaseModel):
    """Model representing a staff member."""

    id: int
    name: str
    rank: Optional[str] = None
    position: Optional[str] = None
    status: StaffStatus

    def __str__(self) -> str:
        """String representation of staff member."""
        if self.rank:
            return f"{self.rank} {self.name}"
        return self.name

    def get_parade_state_entry(self) -> str:
        """Get formatted entry for parade state message."""
        name_display = self.position if self.position and any(pos in self.position for pos in ["Sch Comd", "OC", "CC"]) else str(self)
        return f"{name_display} - {self.status.format_status()}"


class StaffList(BaseModel):
    """Collection of staff members."""

    staff: List[StaffMember] = Field(default_factory=list)

    def count_present(self, period: Optional[str] = None) -> int:
        """Count the number of present staff members.

        Args:
            period: Optional period to count ("AM" or "PM")

        Returns:
            Number of present staff members
        """
        count = 0
        for member in self.staff:
            if period == "AM" and member.status.am_pm_split:
                if member.status.am_status == StatusType.PRESENT:
                    count += 1
            elif period == "PM" and member.status.am_pm_split:
                if member.status.pm_status == StatusType.PRESENT:
                    count += 1
            elif not member.status.am_pm_split and member.status.status_type == StatusType.PRESENT:
                count += 1
        return count