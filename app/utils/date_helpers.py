"""Date-related utility functions."""
import calendar
from datetime import date, datetime, timedelta
from typing import Optional, Tuple

import pytz

from app.config import settings


def get_local_time(timezone: Optional[str] = None) -> datetime:
    """Get the current time in the specified timezone.

    Args:
        timezone: Timezone string (e.g., 'Asia/Singapore')

    Returns:
        Current datetime in the specified timezone
    """
    tz = pytz.timezone(timezone or settings.timezone)
    return datetime.now(tz)


def get_local_date(timezone: Optional[str] = None) -> date:
    """Get the current date in the specified timezone.

    Args:
        timezone: Timezone string (e.g., 'Asia/Singapore')

    Returns:
        Current date in the specified timezone
    """
    return get_local_time(timezone).date()


def format_date(input_date: date, format_str: str = "%d/%m/%Y") -> str:
    """Format a date as a string.

    Args:
        input_date: Date to format
        format_str: Date format string

    Returns:
        Formatted date string
    """
    return input_date.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%d/%m/%Y") -> date:
    """Parse a date string into a date object.

    Args:
        date_str: Date string to parse
        format_str: Date format string

    Returns:
        Parsed date object
    """
    return datetime.strptime(date_str, format_str).date()


def parse_date_with_year(date_str: str) -> date:
    """Parse a date string that may or may not include the year.

    Args:
        date_str: Date string in format DD/MM or DD/MM/YYYY

    Returns:
        Parsed date object
    """
    parts = date_str.split("/")
    
    if len(parts) == 2:  # DD/MM format
        day, month = map(int, parts)
        year = get_local_date().year
        # If the month is earlier than current month, assume it's next year
        if month < get_local_date().month:
            year += 1
    elif len(parts) == 3:  # DD/MM/YYYY format
        day, month, year = map(int, parts)
    else:
        raise ValueError(f"Invalid date format: {date_str}")
    
    return date(year, month, day)


def get_next_weekday(start_date: date, weekday: int) -> date:
    """Get the next occurrence of a specific weekday.

    Args:
        start_date: Starting date
        weekday: Target weekday (0=Monday, 6=Sunday)

    Returns:
        Date of the next occurrence of the specified weekday
    """
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def get_date_range(start_date: date, end_date: date) -> list[date]:
    """Get a list of dates in the given range.

    Args:
        start_date: Start date (inclusive)
        end_date: End date (inclusive)

    Returns:
        List of dates in the range
    """
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]
