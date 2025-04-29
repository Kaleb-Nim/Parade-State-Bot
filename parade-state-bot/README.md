# Parade State Bot

Automated system to generate and send daily parade state attendance reports via Telegram.

## Features

- Fetches staff attendance data from Google Sheets
- Retrieves DI (Duty Instructor) schedules from Telegram chat history
- Formats a comprehensive parade state report
- Sends the report to a designated Telegram channel
- Supports date customization and draft mode

## Requirements

- Python 3.9+
- Google Cloud Platform account with Sheets API enabled
- Telegram Bot API token
- Google Sheets API credentials (service account)

## Installation

### Option 1: Local Setup

1. Clone this repository
2. Run the setup script:
   ```bash
   python setup.py
   ```
3. Edit the `.env` file with your configuration
4. Place your Google API credentials file as `credentials.json` in the project root

### Option 2: Docker Setup

1. Clone this repository
2. Create and configure the `.env` file (copy from `.env.example`)
3. Place your Google API credentials file as `credentials.json` in the project root
4. Build and start the container:
   ```bash
   docker-compose up -d
   ```

## Usage

### Command Line Options

```bash
# Generate and send a parade state for today
python -m app.main

# Generate a draft parade state without sending it
python -m app.main --draft

# Generate a parade state for a specific date
python -m app.main --date 30/04/2025

# Run in debug mode (prints to console)
python -m app.main --debug

```

### Setting Up a Scheduled Task

To run the bot automatically every day, set up a cron job:

```bash
# Edit your crontab
crontab -e

# Add a line to run at 8:00 AM daily
0 8 * * * cd /path/to/parade-state-bot && python -m app.main
```

For Docker:

```bash
# Add a line to run at 8:00 AM daily
0 8 * * * cd /path/to/parade-state-bot && docker-compose run parade-state-bot
```

## Configuration

Configure the bot by editing the `.env` file:

```
# Google Sheets API
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_SHEET_RANGE=Sheet1!A1:Z100

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Application settings
LOG_LEVEL=INFO
TIMEZONE=Asia/Singapore
```

### Active Staff Members

The bot is configured to handle hidden rows in the Google Sheet by using a hardcoded list of row numbers for active staff members. This list is defined in `app/config.py`:

```python
active_staff_rows = [6, 7, 9, 10, 11, 12, 13, 15, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 35, 36, 37]
```

If staff members change, you can update this list directly in the configuration file.

### Google Sheets Implementation

The bot uses pandas for efficient handling of spreadsheet data, which provides:
- More efficient handling of spreadsheet data
- Better support for specific date selection
- Improved parsing of complex status formats
- Enhanced performance for larger datasets

For more details, see [Implementation Details](docs/google_sheets_implementation.md).

## License

MIT License