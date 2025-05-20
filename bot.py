#!/usr/bin/env python
"""Bot entry point for the Parade State Bot."""
import asyncio
import sys
import os
import logging
from dotenv import load_dotenv

# Add the project root to Python's path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

from app.services.bot_handler import BotHandler

async def main():
    """Run the bot."""
    bot_handler = BotHandler()
    await bot_handler.run()

if __name__ == "__main__":
    asyncio.run(main())