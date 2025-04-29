"""Telegram service for interacting with Telegram Bot API."""
import re
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

from loguru import logger
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from app.config import settings
from app.models.duty import DutyInstructor, DutySchedule


class TelegramService:
    """Service for interacting with Telegram Bot API."""

    def __init__(self, token: str = None, chat_id: str = None):
        """Initialize the Telegram service.

        Args:
            token: Telegram bot token
            chat_id: Telegram chat ID
        """
        self.token = token or settings.telegram_bot_token
        self.chat_id = chat_id or settings.telegram_chat_id
        self.bot = Bot(token=self.token)

    async def send_message(self, message: str) -> None:
        """Send a message to the configured chat.

        Args:
            message: The message to send
        """
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
            )
            logger.info(f"Message sent to chat {self.chat_id}")
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {e}")
            raise

    async def fetch_di_list(self) -> DutySchedule:
        """Fetch the duty instructor list from Telegram chat history.

        Returns:
            DutySchedule with parsed DI information
        """
        duty_schedule = DutySchedule()

        try:
            # Get recent messages from the chat
            # Note: This is a simplified approach, in reality you might need pagination
            # or more complex filtering to find the right message with the DI list
            async for message in self.bot.get_chat_history(chat_id=self.chat_id, limit=100):
                # Look for messages that might contain the DI list
                if message.text and "/DI LIST" in message.text.upper():
                    # Parse the DI information from the message
                    di_schedule = self._parse_di_list(message.text)
                    if di_schedule:
                        duty_schedule = di_schedule
                        break

            return duty_schedule
        
        except Exception as e:
            logger.error(f"Error fetching DI list from Telegram: {e}")
            # Return empty schedule on error
            return duty_schedule

    def _parse_di_list(self, message_text: str) -> DutySchedule:
        """Parse duty instructor information from message text.

        Args:
            message_text: The text content of the message

        Returns:
            DutySchedule with parsed information
        """
        schedule = DutySchedule()

        # Regular expression to find date and name patterns
        # Example: "29/04/2025: ME3 Edmund Cheong"
        pattern = r"(\d{1,2}/\d{1,2}(?:/\d{4})?)[:\s]+(\w+)\s+([^\n]+)"
        
        matches = re.finditer(pattern, message_text)
        for match in matches:
            date_str = match.group(1)
            rank = match.group(2)
            name = match.group(3).strip()
            
            # Parse the date
            try:
                if date_str.count('/') == 1:  # DD/MM format
                    day, month = map(int, date_str.split('/'))
                    year = datetime.now().year
                else:  # DD/MM/YYYY format
                    parts = date_str.split('/')
                    day = int(parts[0])
                    month = int(parts[1])
                    year = int(parts[2])
                
                duty_date = date(year, month, day)
                
                # Create DutyInstructor and add to schedule
                di = DutyInstructor(
                    name=name,
                    rank=rank,
                    duty_date=duty_date
                )
                schedule.schedule[duty_date] = di
            
            except Exception as e:
                logger.warning(f"Error parsing date '{date_str}': {e}")
                continue
                
        return schedule

    async def fetch_previous_parade_state(self) -> Optional[str]:
        """Fetch the most recent parade state message from chat history.

        Returns:
            The text of the most recent parade state message, if found
        """
        try:
            # Look for the most recent parade state message
            async for message in self.bot.get_chat_history(chat_id=self.chat_id, limit=50):
                if message.text and "Parade State for" in message.text:
                    return message.text
            
            return None
        
        except Exception as e:
            logger.error(f"Error fetching previous parade state: {e}")
            return None