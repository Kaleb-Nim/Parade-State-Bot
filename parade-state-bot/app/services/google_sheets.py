"""Google Sheets service for fetching staff attendance data."""
import os
import re
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple

import pandas as pd
import numpy as np
from google.oauth2 import service_account
from googleapiclient.discovery import build
from loguru import logger

from app.config import settings
from app.models.staff import (
    StaffMember,
    StaffList,
    StaffStatus,
    StatusType,
    LocationDetail
)


class GoogleSheetsService:
    """Service for interacting with Google Sheets API."""

    def __init__(self, credentials_file: str = None, active_staff_rows: List[int] = None):
        """Initialize the Google Sheets service.

        Args:
            credentials_file: Path to the credentials JSON file
            active_staff_rows: List of row numbers (1-indexed) for active staff members
        """
        self.credentials_file = credentials_file or settings.google_credentials_file
        self.sheet_id = settings.google_sheet_id
        self.range = settings.google_sheet_range
        self.active_staff_rows = active_staff_rows or settings.active_staff_rows
        self.service = self._create_service()
        
        # Status mappings based on logic_google_sheets.md
        self.status_mappings = {
            "1": StatusType.PRESENT,
            "DS OFF": StatusType.OIL,
            "DO Off": StatusType.OIL,
            "OFF": StatusType.OIL,
        }
        
        # Define column indices for AM and PM for the current day
        # These would be updated when processing specific dates
        self.am_col_idx = 0
        self.pm_col_idx = 0

    def _create_service(self):
        """Create and return the Google Sheets service.

        Returns:
            Google Sheets API service
        """
        try:
            # Check if the credentials file exists
            if not os.path.exists(self.credentials_file):
                logger.error(f"Credentials file not found: {self.credentials_file}")
                raise FileNotFoundError(f"Credentials file not found: {self.credentials_file}")

            # Create credentials from the service account file
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
            )

            # Build the service
            service = build("sheets", "v4", credentials=credentials)
            return service

        except Exception as e:
            logger.error(f"Error creating Google Sheets service: {e}")
            raise

    def get_sheet_data(self) -> pd.DataFrame:
        """Fetch data from the Google Sheet and convert to pandas DataFrame.

        Returns:
            DataFrame containing the spreadsheet data
        """
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.sheet_id, range=self.range).execute()
            values = result.get("values", [])

            if not values:
                logger.warning("No data found in the Google Sheet")
                return pd.DataFrame()

            # Convert to pandas DataFrame
            df = pd.DataFrame(values)
            
            # Set the first row as column headers if it contains headers
            if df.shape[0] > 0:
                df = df.rename(columns=df.iloc[0]).drop(df.index[0])
                
            return df

        except Exception as e:
            logger.error(f"Error fetching data from Google Sheet: {e}")
            raise

    def find_date_columns(self, df: pd.DataFrame, target_date: date) -> Tuple[int, int]:
        """Find the AM and PM column indices for a specific date.

        Args:
            df: DataFrame containing the spreadsheet data
            target_date: The date to find columns for

        Returns:
            Tuple of (am_column_index, pm_column_index)
        """
        target_date_str = target_date.strftime("%d/%m/%Y")
        
        # First, try to find exact date match in the header row
        for col in df.columns:
            if target_date_str in str(col):
                # Assuming the next column is PM if this is AM
                col_idx = df.columns.get_loc(col)
                return col_idx, col_idx + 1
        
        # If not found, look for date in the second row (merged cells)
        if len(df) > 0:
            for col in range(len(df.columns)):
                cell_value = str(df.iloc[0, col])
                if target_date_str in cell_value:
                    # Typically dates are in a merged cell that spans AM/PM columns
                    # AM column is the current one, PM is the next
                    return col, col + 1
                
        # If still not found, default to the first AM/PM pair
        # (This would be updated based on actual sheet structure)
        return 1, 2  # Assuming columns 1 and 2 are the first AM/PM pair

    def get_staff_list(self, target_date: Optional[date] = None) -> StaffList:
        """Fetch and parse the staff list from Google Sheets for a specific date.

        Args:
            target_date: The date to get staff status for, defaults to today

        Returns:
            StaffList containing all staff members
        """
        if target_date is None:
            target_date = date.today()
            
        # Get the sheet data as DataFrame
        df = self.get_sheet_data()
        
        # Find the columns for the target date
        self.am_col_idx, self.pm_col_idx = self.find_date_columns(df, target_date)
        
        # Extract staff data for active rows
        staff_list = self._extract_staff_data(df, target_date)
        
        return staff_list

    def _extract_staff_data(self, df: pd.DataFrame, target_date: date) -> StaffList:
        """Extract staff data from the DataFrame.

        Args:
            df: DataFrame containing the sheet data
            target_date: The target date for the status

        Returns:
            StaffList containing all staff members
        """
        staff_list = StaffList()
        
        try:
            # Process only the active staff rows
            for staff_index, row_num in enumerate(sorted(self.active_staff_rows), 1):
                # Convert to 0-indexed for DataFrame
                df_row_idx = row_num - 1
                
                # Skip if row doesn't exist in DataFrame
                if df_row_idx < 0 or df_row_idx >= len(df):
                    logger.warning(f"Row {row_num} is out of range for the sheet data")
                    continue
                
                # Extract staff info from row
                name = str(df.iloc[df_row_idx, 0]) if 0 < len(df.columns) else ""
                
                # Get AM and PM status
                am_status_str = str(df.iloc[df_row_idx, self.am_col_idx]) if self.am_col_idx < len(df.columns) else "P"
                pm_status_str = str(df.iloc[df_row_idx, self.pm_col_idx]) if self.pm_col_idx < len(df.columns) else "P"
                
                # Clean status strings
                am_status_str = am_status_str.strip() if not pd.isna(am_status_str) else "P"
                pm_status_str = pm_status_str.strip() if not pd.isna(pm_status_str) else "P"
                
                # Check if AM/PM are different
                am_pm_split = (am_status_str != pm_status_str) and (am_status_str != "" and pm_status_str != "")
                
                # Create the status object
                staff_status = self._create_staff_status(am_status_str, pm_status_str, am_pm_split)
                
                # Determine position and rank from name if necessary
                position = None
                rank = None
                
                # Special positions like "Sch Comd", "OC MECH", etc.
                if "Sch Comd" in name or "OC" in name or "CC" in name:
                    position = name
                else:
                    # Extract rank if present (typical military ranks like ME3, etc.)
                    rank_match = re.match(r'^(ME\d+|LTC|MAJ|CPT|LTA)\s+(.+)$', name)
                    if rank_match:
                        rank = rank_match.group(1)
                        name = rank_match.group(2)
                    
                # Create the staff member
                staff = StaffMember(
                    id=staff_index,
                    name=name,
                    rank=rank,
                    position=position,
                    status=staff_status,
                )
                
                staff_list.staff.append(staff)
            
            # Log warning if no staff were found
            if not staff_list.staff:
                logger.warning("No active staff members were found in the specified rows")
                
            return staff_list
            
        except Exception as e:
            logger.error(f"Error extracting staff data: {e}")
            raise

    def _create_staff_status(self, am_status_str: str, pm_status_str: str, am_pm_split: bool) -> StaffStatus:
        """Create a StaffStatus object from AM and PM status strings.

        Args:
            am_status_str: Status string for AM
            pm_status_str: Status string for PM
            am_pm_split: Whether AM and PM statuses are different

        Returns:
            StaffStatus object
        """
        if not am_pm_split:
            # Use AM status as the overall status
            return self._parse_status_string(am_status_str)
        
        # Handle AM/PM split
        am_status = self._parse_status_string(am_status_str)
        pm_status = self._parse_status_string(pm_status_str)
        
        # Create combined status
        combined_status = StaffStatus(
            status_type=am_status.status_type,  # Default to AM status type
            am_pm_split=True,
            am_status=am_status.status_type,
            am_location=am_status.location,
            pm_status=pm_status.status_type,
            pm_location=pm_status.location,
            end_date=pm_status.end_date or am_status.end_date,
        )
        
        return combined_status

    def _parse_status_string(self, status_str: str) -> StaffStatus:
        """Parse a status string into a StaffStatus object.

        Args:
            status_str: Status string from the spreadsheet

        Returns:
            StaffStatus object
        """
        # Default status
        status_type = StatusType.PRESENT
        location_detail = None
        end_date = None
        details = None
        
        # Handle empty or NaN status
        if not status_str or status_str == "nan" or status_str == "":
            return StaffStatus(status_type=status_type)
        
        # Apply status mappings
        if status_str in self.status_mappings:
            status_type = self.status_mappings[status_str]
            
            # Handle special cases with details
            if status_str == "DS OFF":
                details = "(DS OFF)"
            elif status_str == "DO Off":
                details = "(DO OFF)"
                
            return StaffStatus(
                status_type=status_type,
                details=details
            )
        
        # Extract location if @ symbol is present
        if "@" in status_str:
            status_parts = status_str.split("@", 1)
            status_part = status_parts[0].strip()
            location_part = status_parts[1].strip()
            
            # Check for status type
            for status in StatusType:
                if status.value in status_part:
                    status_type = status
                    break
            
            # Create location detail
            location_detail = LocationDetail(
                location=location_part,
                detail=None
            )
            
            return StaffStatus(
                status_type=status_type,
                location=location_detail
            )
            
        # Handle status with TILL (end date)
        if "TILL" in status_str:
            parts = status_str.split("TILL")
            status_part = parts[0].strip()
            date_part = parts[1].strip()
            
            # Find status type
            for status in StatusType:
                if status.value in status_part:
                    status_type = status
                    break
            
            # Parse date
            try:
                # Assuming date format is DD/MM
                day, month = date_part.split("/")
                current_year = datetime.now().year
                # If the month is less than the current month, it's likely next year
                year = current_year if int(month) >= datetime.now().month else current_year + 1
                end_date = date(year, int(month), int(day))
            except Exception as e:
                logger.warning(f"Could not parse date from '{date_part}': {e}")
            
            return StaffStatus(
                status_type=status_type,
                end_date=end_date
            )
        
        # Handle standard status types
        for status in StatusType:
            if status.value == status_str:
                return StaffStatus(status_type=status)
        
        # Default to OTHERS for unrecognized status
        return StaffStatus(
            status_type=StatusType.OTHERS,
            details=status_str
        )