"""Configuration management for the Parade State Bot."""
import os
from typing import Optional, List

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

print(f'env variables loaded {load_dotenv()}')


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Sheets API
    google_credentials_file: str = Field(
        default=os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json"),
        description="Path to the Google API credentials JSON file",
    )
    google_sheet_id: str = Field(
        default=os.getenv("GOOGLE_SHEET_ID", ""),
        description="Google Sheet ID for the attendance data",
    )
    google_sheet_range: str = Field(
        default=os.getenv("GOOGLE_SHEET_RANGE", "Sheet1!A1:Z100"),
        description="Range of cells to read from the Google Sheet",
    )
    google_sheet_range_names:str = Field(
        default= os.getenv("GOOGLE_SHEET_RANGE_NAMES", "Sheet1!A1:A40"),
        description = "Just the name list, so that we dont have to read 2years of redundent information"
    )
    
    # Active staff rows configuration
    # These are the row numbers (1-indexed) in the Google Sheet for active staff members
    active_staff_rows: List[int] = Field(
        default=[6, 7, 9, 10, 11, 12, 13, 15, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 35, 36, 37],
        description="Row numbers (1-indexed) of active staff members in the Google Sheet",
    )

    # Telegram Bot
    telegram_bot_token: str = Field(
        default=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        description="Telegram Bot API token",
    )
    telegram_chat_id: str = Field(
        default=os.getenv("TELEGRAM_CHAT_ID", ""),
        description="Telegram chat ID where parade state will be sent",
    )

    # Application settings
    log_level: str = Field(
        default=os.getenv("LOG_LEVEL", "INFO"),
        description="Logging level",
    )
    timezone: str = Field(
        default=os.getenv("TIMEZONE", "Asia/Singapore"),
        description="Timezone for date calculations",
    )

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


# Create a global instance of settings
settings = Settings()
