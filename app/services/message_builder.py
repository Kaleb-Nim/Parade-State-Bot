"""Service for building parade state messages."""
from datetime import date, datetime, timedelta
from typing import Optional

from loguru import logger

from app.models.duty import DutyInstructor, DutySchedule
from app.models.parade_state import ParadeState
from app.models.staff import StaffList
from app.services.google_sheets import GoogleSheetsService
from app.services.telegram_service import TelegramService


class MessageBuilderService:
    """Service for building parade state messages."""

    def __init__(
        self,
        google_sheets_service: GoogleSheetsService,
        telegram_service: TelegramService,
    ):
        """Initialize the message builder service.

        Args:
            google_sheets_service: Service for Google Sheets operations
            telegram_service: Service for Telegram operations
        """
        self.google_sheets_service = google_sheets_service
        self.telegram_service = telegram_service

    async def build_parade_state(self, target_date: Optional[date] = None) -> ParadeState:
        """Build a parade state for the specified date.

        Args:
            target_date: The date for the parade state, defaults to today

        Returns:
            ParadeState containing all necessary information
        """
        # Use today's date if not specified
        if target_date is None:
            target_date = date.today()

        try:
            # Fetch staff data from Google Sheets
            staff_list = self.google_sheets_service.get_staff_list(target_date=target_date)

            # Fetch DI schedule from Telegram
            duty_schedule = await self.telegram_service.fetch_di_list()

            # Get the current and next DI
            current_di = duty_schedule.get_di_for_date(target_date)
            next_di = duty_schedule.get_next_di(target_date)

            # Create the parade state
            parade_state = ParadeState(
                report_date=target_date,
                staff_list=staff_list,
                current_di=current_di,
                next_di=next_di,
            )

            return parade_state

        except Exception as e:
            logger.error(f"Error building parade state: {e}")
            raise

    async def generate_message(self, target_date: Optional[date] = None) -> str:
        """Generate a formatted parade state message.

        Args:
            target_date: The date for the parade state, defaults to today

        Returns:
            Formatted parade state message
        """
        parade_state = await self.build_parade_state(target_date)
        return parade_state.format_message()