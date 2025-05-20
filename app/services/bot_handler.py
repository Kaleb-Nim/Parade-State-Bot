"""Telegram bot command handler."""
import asyncio
from datetime import date
from typing import Optional

from loguru import logger
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.config import settings
from app.services.message_builder import MessageBuilderService
from app.services.google_sheets import GoogleSheetsService
from app.services.telegram_service import TelegramService

class BotHandler:
    """Handler for Telegram bot commands."""

    def __init__(self):
        """Initialize the bot handler."""
        self.token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.application = Application.builder().token(self.token).build()
        
        # Set up services
        self.google_sheets_service = GoogleSheetsService()
        self.telegram_service = TelegramService()
        self.message_builder = MessageBuilderService(
            google_sheets_service=self.google_sheets_service,
            telegram_service=self.telegram_service
        )
        
        # Register command handlers
        self.application.add_handler(CommandHandler("draft", self.handle_draft))
        self.application.add_handler(CommandHandler("send", self.handle_send))
        self.application.add_handler(CommandHandler("help", self.handle_help))

    async def handle_draft(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /draft command - generate a parade state draft."""
        try:
            chat_id = update.effective_chat.id
            logger.info(f"Draft command received from chat {chat_id}")
            
            # Generate the parade state message
            message = await self.message_builder.generate_message()
            
            # Send as a reply
            await update.message.reply_text(
                text="📋 Draft Parade State:\n\n" + message
            )
            
            logger.info(f"Draft sent to chat {chat_id}")
        except Exception as e:
            logger.error(f"Error handling draft command: {e}")
            await update.message.reply_text(f"Error generating draft: {str(e)}")

    async def handle_send(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /send command - send parade state to configured chat."""
        try:
            chat_id = update.effective_chat.id
            logger.info(f"Send command received from chat {chat_id}")
            
            # Generate the parade state message
            message = await self.message_builder.generate_message()
            
            # Send to configured chat
            await self.telegram_service.send_message(message)
            
            # Confirm to the user
            await update.message.reply_text("✅ Parade state sent to the configured channel.")
            
            logger.info(f"Parade state sent to configured chat {self.chat_id}")
        except Exception as e:
            logger.error(f"Error handling send command: {e}")
            await update.message.reply_text(f"Error sending parade state: {str(e)}")

    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command - show available commands."""
        help_text = """
Available commands:

/draft - Generate and see a draft of today's parade state
/send - Send today's parade state to the configured channel
/help - Show this help message
        """
        await update.message.reply_text(help_text)

    async def run(self) -> None:
        """Run the bot."""
        logger.info("Starting Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        try:
            # Keep the bot running
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Stopping Telegram bot...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()