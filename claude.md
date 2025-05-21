# Parade State Bot - Development Specifications

## Overview
Automating the daily task of sending parade state attendance for 24 permanent staff members via Telegram.

### Task Requirements
- Send out parade state attendance daily
- Format output as a structured Telegram message
- Include:
  * Date
  * Today's duty instructor (DI)
  * Next duty instructor
  * Status/location of all 24 staff members (with end date of leaves, AM/PM splits if needed)
  * Attendance count for AM/PM

## Implementation Status

### Completed
1. **Project Structure and Architecture**
   - Directory structure following Python best practices
   - Configuration management with environment variables
   - Clean separation of concerns (models, services, utilities)

2. **Core Data Models**
   - Staff member representations with Pydantic
   - Status types and complex status formatting
   - Location details with proper formatting
   - Parade state report generation

3. **Service Implementations**
   - Google Sheets service for fetching staff data
   - Telegram service for message delivery
   - Message builder service for generating formatted reports

### Special Considerations
- **Hidden Rows in Google Sheet**: The spreadsheet has hidden rows for inactive staff. We handle this by using a hardcoded list of active row numbers in `config.py`:
  ```python
  active_staff_rows = [6, 7, 9, 10, 11, 12, 13, 15, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 35, 36, 37]
  ```

- **Complex Status Formats**: Staff status can appear in various formats:
  - Simple: `P` (Present)
  - With end date: `CSE TILL 09/05`
  - With location: `MA @ NATIONAL SKIN CENTRE`
  - AM/PM split: `P(AM), OTH LEARNING DAY(PM)`
  - Complex: `RS @ ONE CARE HMI CLINIC TAMPINIES (AM), MC (PM)`

## Data Sources
1. **Google Spreadsheet**
   - Contains staff names and status
   - Sheet link: https://docs.google.com/spreadsheets/d/1RQtU7wR7EMkaLgs6gkEbF742YXuID0n99YwMC8fnxQI/edit

2. **AES Bot**
   - Use `/DI LIST` command to get DI schedule

3. **Telegram Chat History**
   - Previous parade state messages
   - Chat ID: `-1764119725`

## Example Final Output
```
Parade State for 29/04/2025
Tuesday

Today's DI: ME3 Edmund Cheong
Next DI: ME3 Jonathan Koe

1. Sch Comd - P
2. OC MECH - P
3. OC EW - P
4. CC - CSE TILL 09/05
5. Edwin - CPE TILL 30/04
6. Jeffrey - OL TILL 02/05
7. Or LW - HL TILL 09/05
8. Marcus - WFH
9. Boon Hwee - P
10. Leonard - P
11. Gin - P
12. Wilfred - P
13. Edmund Cheong - P
14. Jonathan - OL TILL 29/04
15. Benson - P(AM), OB@SBAB(PM)
16. Edmund Yeo - P
17. Thian Kiong - P
18. Tan Kok Kuan - P
19. Derrick Tan - P
20. Magendran - P
21. Tan Eng Chuan - P
22. Chen Yiming - P
23. Sherwyn Sim - P
24. Kaleb Nim - P

Today's number: 18(AM), 18(PM)
```

* If the location of status is different between morning and afternoon, it will be shown as `LOCATION(AM), LOCATION(PM)`.
* If the status is the same for both AM and PM, no need to show AM/PM.

## Status Types
The system recognizes various status types:
- `P` - Present
- `CSE` - Course
- `CPE` - Course Preparation Exercise
- `OL` - Off Labor
- `OML` - Off Medical Leave
- `LL` - Local Leave
- `HL` - Hospitalization Leave
- `WFH` - Work From Home
- `WAH` - Work At Home
- `MC` - Medical Certificate
- `LEAVE` - Annual Leave
- `ABS` - Absent
- `OIL` - Off-In-Lieu
- `DO` - Day Off
- `ACE` - Annual cohesion exercise
- `FPUL` - Family preparation urgent leave
- `FCL` - Family care leave
- `MA` - Medical Appointment
- `RS` - Regular Screening
- `OB` - Out Bounds / Official Business
- `AO` - Attached Out
- `OTH` - Other
- `DS` - DS Off / Duty Staff
- `OTHERS` - Catch-all for unrecognized status

## Project Structure

```
parade-state-bot/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration handling
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── staff.py            # Staff member models
│   │   ├── parade_state.py     # Parade state models
│   │   └── duty.py             # DI duty models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── google_sheets.py    # Google Sheets API integration
│   │   ├── telegram.py         # Telegram Bot API integration
│   │   └── message_builder.py  # Message formatting logic
│   └── utils/
│       ├── __init__.py
│       ├── date_helpers.py     # Date manipulation utilities
│       └── formatters.py       # Text formatting utilities
├── tests/                      # Unit and integration tests
├── .env.example                # Example environment variables
├── requirements.txt            # Project dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker compose configuration
└── README.md                   # Project documentation
```

## Development Environment Setup
1. Create and activate a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure settings
4. Set up Google Sheets API credentials
5. Set up Telegram Bot API token

## Configuration
```
# Google Sheets API
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=1RQtU7wR7EMkaLgs6gkEbF742YXuID0n99YwMC8fnxQI
GOOGLE_SHEET_RANGE=Sheet1!A1:Z100

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=-1764119725

# Application settings
LOG_LEVEL=INFO
TIMEZONE=Asia/Singapore
```

## Running the Bot
```bash
# Generate and send a parade state for today
python -m app.main

# Generate a draft without sending
python -m app.main --draft

# Generate for a specific date
python -m app.main --date 30/04/2025

# Debug mode (prints to console)
python -m app.main --debug
```

## Upcoming Work
- Implement tests
- Improve error handling
- Add support for edge cases in status parsing
- Implement deployment workflow
- Add monitoring and logging improvements

## Code Style Guidelines
- Follow PEP 8 conventions
- Use Pydantic models for all data structures
- Order imports: standard library → third-party → local modules
- Include type annotations for all function parameters and returns
- Use snake_case for variables/functions, PascalCase for classes
- Create separate files for different functional classes
- Include docstrings for all classes and functions

## Claude context
- Read all claude_history and add to context window