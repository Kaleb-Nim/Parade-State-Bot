"""Models for the parade state report."""
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.duty import DutyInstructor
from app.models.staff import StaffList, StaffMember


class ParadeState(BaseModel):
    """Model representing a parade state report."""

    report_date: date
    staff_list: StaffList
    current_di: Optional[DutyInstructor] = None
    next_di: Optional[DutyInstructor] = None
    am_count: int = 0
    pm_count: int = 0

    def __init__(self, **data):
        """Initialize the parade state and calculate attendance counts."""
        super().__init__(**data)
        self.calculate_counts()

    def calculate_counts(self) -> None:
        """Calculate the present counts for AM and PM."""
        self.am_count = self.staff_list.count_present(period="AM")
        self.pm_count = self.staff_list.count_present(period="PM")

    def format_message(self) -> str:
        """Format the complete parade state message."""
        # Get day name
        day_name = self.report_date.strftime("%A")

        # Format the header
        header = [
            f"Parade State for {self.report_date.strftime('%d/%m/%Y')}",
            day_name,
            "",
        ]

        # Add DI information
        di_info = []
        if self.current_di:
            di_info.append(f"Today's DI: {self.current_di}")
        if self.next_di:
            di_info.append(f"Next DI: {self.next_di}")
        di_info.append("")

        # Format staff list
        staff_entries = []
        for i, staff in enumerate(self.staff_list.staff, 1):
            staff_entries.append(f"{i}. {staff.get_parade_state_entry()}")
        staff_entries.append("")

        # Add attendance counts
        counts = [f"Today's number: {self.am_count}(AM), {self.pm_count}(PM)"]

        # Combine all sections
        message_parts = header + di_info + staff_entries + counts
        return "\n".join(message_parts)