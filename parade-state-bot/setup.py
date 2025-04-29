#!/usr/bin/env python
"""Setup script for Parade State Bot."""
import os
import sys
from shutil import copyfile

# Create .env file from .env.example if it doesn't exist
if not os.path.exists(".env") and os.path.exists(".env.example"):
    print("Creating .env file from .env.example...")
    copyfile(".env.example", ".env")
    print("Please edit the .env file to configure your environment variables.")

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    print("Creating logs directory...")
    os.makedirs("logs")

# Check if credentials.json exists
if not os.path.exists("credentials.json"):
    print(
        "WARNING: credentials.json not found. Please download your Google API credentials "
        "file and save it as credentials.json in the project root directory."
    )

# Install dependencies
print("Installing dependencies...")
os.system(f"{sys.executable} -m pip install -r requirements.txt")

print(
    """
Setup complete!

To run the bot:
- Edit the .env file with your configuration
- Place your Google API credentials file as credentials.json in the project root
- Run the bot with: python -m app.main

To run in docker:
- docker-compose up -d
    """
)