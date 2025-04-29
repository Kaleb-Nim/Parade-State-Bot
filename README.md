# Parade State Bot

Automated system for generating and sending daily parade state attendance reports via Telegram.

## Overview

This bot automates the daily task of sending parade state attendance for 24 permanent staff members. It collects data from Google Sheets, processes it, and formats a structured Telegram message with:

- Date information
- Today's duty instructor (DI)
- Next duty instructor
- Locations/status of all staff members (including end duration of CSE/MC)
- Attendance numbers for AM/PM periods

## Project Structure

The project follows a clean architecture approach with separated responsibilities:

- **Models**: Pydantic models for data representation
- **Services**: Core business logic and external API integrations
- **Utils**: Helper functions and utilities

## Data Flow

The application processes data as follows:

1. Retrieves staff attendance data from Google Sheets
2. Fetches duty instructor information from Telegram bot history
3. Processes and formats the data into a structured parade state message
4. Sends the message to the designated Telegram channel

## Documentation

For detailed technical documentation, see:

- [Technical Plan](./technical_plan.md) - Overall implementation plan
- [Data Flow Diagram](./dataflow.md) - Visual representation of the data flow
- [Code Documentation](./parade-state-bot/README.md) - Specific code implementation details

## Getting Started

See the [Code Documentation](./parade-state-bot/README.md) for detailed setup and usage instructions.

## License

MIT License