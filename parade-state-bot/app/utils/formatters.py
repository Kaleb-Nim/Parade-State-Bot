"""Text formatting utilities."""
import re
from typing import List, Dict, Any


def format_name_with_rank(name: str, rank: str = "") -> str:
    """Format a name with its rank.

    Args:
        name: Person's name
        rank: Military rank

    Returns:
        Formatted name with rank
    """
    if not rank:
        return name
    return f"{rank} {name}".strip()


def format_status_with_date(status: str, end_date: str = "") -> str:
    """Format a status with an end date.

    Args:
        status: Status code
        end_date: End date in DD/MM format

    Returns:
        Formatted status string
    """
    if not end_date:
        return status
    return f"{status} TILL {end_date}"


def format_count(am_count: int, pm_count: int) -> str:
    """Format the attendance count for the parade state.

    Args:
        am_count: Morning attendance count
        pm_count: Afternoon attendance count

    Returns:
        Formatted count string
    """
    return f"Today's number: {am_count}(AM), {pm_count}(PM)"


def clean_text(text: str) -> str:
    """Clean text by removing excessive whitespace and normalizing newlines.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    # Replace multiple spaces with a single space
    text = re.sub(r" +", " ", text)
    
    # Replace multiple newlines with at most two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    # Trim leading/trailing whitespace
    return text.strip()