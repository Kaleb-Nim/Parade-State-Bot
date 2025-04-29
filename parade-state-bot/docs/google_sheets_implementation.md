# Google Sheets Service Implementation

This document explains the implementation of the Google Sheets service for the Parade State Bot using pandas for efficient data handling.

## Overview

The `GoogleSheetsService` leverages the pandas library for data manipulation, offering the following advantages:

- More efficient data handling for spreadsheets
- Simplified date-based column selection
- Better support for handling missing values and data types
- Improved performance for larger spreadsheets
- Simplified mapping between spreadsheet values and status types

## Key Features

1. **DataFrame-based Processing**: 
   - Converts the raw Google Sheets data into a pandas DataFrame for easier manipulation
   - Simplifies row and column selection

2. **Date-based Column Selection**:
   - Automatically finds the AM/PM columns for a specific date
   - Handles merged cells in the date headers

3. **Optimized Status Parsing**:
   - Maps special values like "1" to "Present"
   - Handles DS OFF, DO Off, and other special statuses
   - Efficiently parses complex status strings

4. **Direct Pandas Integration**:
   - Uses pandas' built-in handling for null values and missing data
   - Leverages pandas' vectorized operations for better performance

## How It Works

1. The service retrieves data from Google Sheets API
2. The raw data is converted to a pandas DataFrame
3. The service identifies the relevant columns for the requested date
4. It processes only the active staff rows (configurable list)
5. Status values are parsed and converted to StaffStatus objects
6. The service returns a structured StaffList object

## Status Mappings

The service includes special mappings for Google Sheets values:

```python
self.status_mappings = {
    "1": StatusType.PRESENT,
    "DS OFF": StatusType.OIL,
    "DO Off": StatusType.OIL,
    "OFF": StatusType.OIL,
}
```

These mappings handle common cases from the Google Sheet:
- "1" in the sheet represents "Present" (P) in the final message
- "DS OFF" is mapped to "OIL (DS OFF)"
- "DO Off" is mapped to "OIL (DO OFF)"
- "OFF" is mapped to "OIL"

## Usage

```python
# Generate a parade state
python -m app.main

# Generate a draft 
python -m app.main --draft

# Generate for a specific date
python -m app.main --date 30/04/2025
```

## Implementation Details

### Finding Date Columns

The service includes a `find_date_columns` method that identifies the AM/PM columns for a specific date:

```python
def find_date_columns(self, df: pd.DataFrame, target_date: date) -> Tuple[int, int]:
    """Find the AM and PM column indices for a specific date."""
    # Searches for the target date in sheet headers
    # and returns the column indices for AM/PM columns
```

### Processing Active Staff Rows

The service only processes rows specified in the active_staff_rows configuration:

```python
def _extract_staff_data(self, df: pd.DataFrame, target_date: date) -> StaffList:
    """Extract staff data from the DataFrame."""
    # Processes only active staff rows
    for staff_index, row_num in enumerate(sorted(self.active_staff_rows), 1):
        # Extract data for each active staff row
```

### Status Parsing Logic

The service includes robust parsing for status strings:

```python
def _parse_status_string(self, status_str: str) -> StaffStatus:
    """Parse a status string into a StaffStatus object."""
    # Handles special mappings
    # Extracts location details
    # Parses end dates
```

## Requirements

The pandas implementation requires additional dependencies:
- pandas>=1.3.0
- numpy>=1.20.0

## Performance Considerations

The pandas implementation is particularly beneficial when:
- Processing large spreadsheets
- Working with complex data structures
- Handling missing or inconsistent data
- Needing to filter data based on dates or other criteria

For very small datasets, the performance difference may not be significant.