"""Main entry point for the Parade State Bot application."""
import asyncio
import os
import argparse
from datetime import date, datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from loguru import logger

from app.config import settings
from app.models.parade_state import ParadeState
from app.services.google_sheets import GoogleSheetsService
from app.services.message_builder import MessageBuilderService
from app.services.telegram_service import TelegramService
from app.utils.date_helpers import get_local_date

# Load environment variables
load_dotenv()

# Set up logging
logger.add(
    "logs/parade_state_{time}.log",
    rotation="1 day",
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)


async def send_parade_state(target_date: Optional[date] = None) -> None:
    """Send the parade state message.

    Args:
        target_date: The date for the parade state, defaults to today
    """
    try:
        # Use current date if not specified
        if target_date is None:
            target_date = get_local_date()

        logger.info(f"Generating parade state for {target_date}")

        # Initialize services
        google_sheets_service = GoogleSheetsService()
        telegram_service = TelegramService()
        message_builder_service = MessageBuilderService(
            google_sheets_service=google_sheets_service,
            telegram_service=telegram_service,
        )

        # Generate the parade state message
        message = await message_builder_service.generate_message(target_date)

        # Send the message to Telegram
        await telegram_service.send_message(message)

        logger.success(f"Parade state sent successfully for {target_date}")

    except Exception as e:
        logger.error(f"Error sending parade state: {e}")
        raise


async def generate_draft_parade_state(target_date: Optional[date] = None) -> str:
    """Generate a draft parade state message without sending it.

    Args:
        target_date: The date for the parade state, defaults to today

    Returns:
        The formatted parade state message
    """
    try:
        # Use current date if not specified
        if target_date is None:
            target_date = get_local_date()

        logger.info(f"Generating draft parade state for {target_date}")

        # Initialize services
        google_sheets_service = GoogleSheetsService()
        telegram_service = TelegramService()
        message_builder_service = MessageBuilderService(
            google_sheets_service=google_sheets_service,
            telegram_service=telegram_service,
        )

        # Generate the parade state message
        message = await message_builder_service.generate_message(target_date)

        logger.success(f"Draft parade state generated successfully for {target_date}")
        return message

    except Exception as e:
        logger.error(f"Error generating draft parade state: {e}")
        raise


async def main() -> None:
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description="Parade State Bot")
    parser.add_argument(
        "--date", 
        type=str, 
        help="Target date in DD/MM/YYYY format (default: today)"
    )
    parser.add_argument(
        "--draft", 
        action="store_true", 
        help="Generate a draft without sending it"
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Run in debug mode (prints to console)"
    )
    
    args = parser.parse_args()
    
    # Parse target date if provided
    target_date = None
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%d/%m/%Y").date()
        except ValueError:
            logger.error(f"Invalid date format: {args.date}. Use DD/MM/YYYY format.")
            return
    
    # Run in draft or send mode
    try:
        if args.draft or args.debug:
            message = await generate_draft_parade_state(target_date)
            print("\n" + "=" * 50)
            print("DRAFT PARADE STATE:")
            print("=" * 50)
            print(message)
            print("=" * 50 + "\n")
        else:
            await send_parade_state(target_date)
    except Exception as e:
        logger.error(f"Application error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
