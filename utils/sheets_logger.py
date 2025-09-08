"""
Google Sheets logging service for production environment
"""
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
from utils.logger import info, warning, error

class GoogleSheetsLogger:
    """Logging service that writes logs to Google Sheets in production"""
    
    def __init__(self):
        self.worksheet_name = "application_logs"
        self.credentials = None
        self.worksheet = None
        self.is_available = False
        self._setup_connection()
    
    def _setup_connection(self):
        """Setup Google Sheets connection for logging"""
        try:
            # Try to get credentials from Streamlit secrets
            if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
                creds_info = st.secrets['google_sheets']
                spreadsheet_id = st.secrets['google_sheets']['spreadsheet_id']
                
                # Create a copy of creds_info since st.secrets is read-only
                creds_info_copy = dict(creds_info)
                
                # Ensure private key is properly formatted
                if 'private_key' in creds_info_copy:
                    creds_info_copy['private_key'] = creds_info_copy['private_key'].replace('\\n', '\n')
                
                credentials = Credentials.from_service_account_info(
                    creds_info_copy,
                    scopes=['https://www.googleapis.com/auth/spreadsheets',
                           'https://www.googleapis.com/auth/drive']
                )
                
                # Initialize the Google Sheets client
                gc = gspread.authorize(credentials)
                
                # Open the spreadsheet
                spreadsheet = gc.open_by_key(spreadsheet_id)
                
                # Try to get the logs worksheet, create if it doesn't exist
                try:
                    self.worksheet = spreadsheet.worksheet(self.worksheet_name)
                except gspread.WorksheetNotFound:
                    # Create the logs worksheet
                    self.worksheet = spreadsheet.add_worksheet(
                        title=self.worksheet_name, 
                        rows=1000, 
                        cols=6
                    )
                    # Set up headers
                    headers = ['Timestamp', 'Level', 'Message', 'Function', 'Context', 'Error_Details']
                    self.worksheet.append_row(headers)
                    info(f"Created logs worksheet: {self.worksheet_name}")
                
                self.is_available = True
                info("Google Sheets logging initialized successfully")
                
            else:
                warning("No Google Sheets credentials found. Logging to sheets disabled.")
                self.is_available = False
                
        except Exception as e:
            error(f"Failed to setup Google Sheets logging: {e}")
            self.is_available = False
    
    def log(self, level, message, function_name=None, context=None, error_details=None):
        """Log a message to Google Sheets"""
        if not self.is_available:
            return False
        
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Prepare log row
            log_row = [
                timestamp,
                level.upper(),
                str(message)[:500],  # Limit message length
                function_name or '',
                str(context)[:200] if context else '',  # Limit context length
                str(error_details)[:500] if error_details else ''  # Limit error details
            ]
            
            # Append to worksheet
            self.worksheet.append_row(log_row)
            return True
            
        except Exception as e:
            error(f"Failed to write log to Google Sheets: {e}")
            return False
    
    def get_recent_logs(self, limit=100):
        """Get recent logs from Google Sheets"""
        if not self.is_available:
            return []
        
        try:
            # Get all records
            records = self.worksheet.get_all_records()
            
            # Sort by timestamp (assuming first column is timestamp)
            records.sort(key=lambda x: x.get('Timestamp', ''), reverse=True)
            
            # Return limited number
            return records[:limit]
            
        except Exception as e:
            error(f"Failed to read logs from Google Sheets: {e}")
            return []
    
    def clear_logs(self):
        """Clear all logs from the worksheet"""
        if not self.is_available:
            return False
        
        try:
            # Clear all data except headers
            self.worksheet.clear()
            
            # Re-add headers
            headers = ['Timestamp', 'Level', 'Message', 'Function', 'Context', 'Error_Details']
            self.worksheet.append_row(headers)
            
            info("Cleared all logs from Google Sheets")
            return True
            
        except Exception as e:
            error(f"Failed to clear logs from Google Sheets: {e}")
            return False

# Global instance
sheets_logger = GoogleSheetsLogger()
