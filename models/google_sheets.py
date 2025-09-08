import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
from datetime import date
import json

class GoogleSheetsService:
    def __init__(self):
        self.worksheet_name = "case_records"
        self.credentials = None
        self.gc = None
        self.worksheet = None
        self.is_mock = False
        self.mock_data = []
        self._setup_connection()
    
    def _setup_connection(self):
        """Setup Google Sheets connection using service account credentials"""
        try:
            # Always try to get credentials from Streamlit secrets first
            if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
                creds_info = st.secrets['google_sheets']
                spreadsheet_id = st.secrets['google_sheets']['spreadsheet_id']
                st.info("🔧 Using credentials from Streamlit secrets")
                st.info(f"📊 Spreadsheet ID: {spreadsheet_id}")
            else:
                st.warning("⚠️ No Streamlit secrets found. Using mock data for demonstration.")
                st.info("💡 **To fix this**: Create a `.streamlit/secrets.toml` file with your Google Sheets credentials")
                self._use_mock_data()
                return
            
            if spreadsheet_id == 'demo_spreadsheet' or not spreadsheet_id:
                st.warning("⚠️ Spreadsheet ID not configured. Using mock data for demonstration.")
                self._use_mock_data()
                return
            
            # Get credentials
            # Create a copy of creds_info since st.secrets is read-only
            creds_info_copy = dict(creds_info)
            
            # Ensure private key is properly formatted
            if 'private_key' in creds_info_copy:
                # Replace literal \n with actual newlines
                creds_info_copy['private_key'] = creds_info_copy['private_key'].replace('\\n', '\n')
            
            credentials = Credentials.from_service_account_info(
                creds_info_copy,
                scopes=['https://www.googleapis.com/auth/spreadsheets', 
                       'https://www.googleapis.com/auth/drive']
            )
            
            self.gc = gspread.authorize(credentials)
            
            # Try to open the spreadsheet
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            self.worksheet = spreadsheet.worksheet(self.worksheet_name)
            
            st.success("✅ Successfully connected to Google Sheets!")
            
        except Exception as e:
            error_msg = str(e)
            if "Incorrect padding" in error_msg:
                st.error("🔑 **Google Sheets Authentication Error**: Incorrect private key format. Please check your credentials.")
                st.info("💡 **Tip**: Make sure the private key in your secrets file has proper newline characters (\\n)")
            elif "invalid_grant" in error_msg:
                st.error("🔑 **Google Sheets Authentication Error**: Invalid credentials. Please check your service account key.")
            elif "access_denied" in error_msg:
                st.error("🔑 **Google Sheets Authentication Error**: Access denied. Please check if the service account has access to the spreadsheet.")
            else:
                st.warning(f"⚠️ Could not connect to Google Sheets: {e}")
            
            st.info("🔄 Using mock data for demonstration. Check your credentials to connect to Google Sheets.")
            self._use_mock_data()
    
    def _use_mock_data(self):
        """Use mock data when Google Sheets is not available"""
        self.mock_data = []
        self.is_mock = True
    
    def _get_all_records(self):
        """Get all records from the worksheet"""
        if self.is_mock:
            return self.mock_data
        
        try:
            records = self.worksheet.get_all_records()
            # Convert empty strings to None for better handling
            for record in records:
                for key, value in record.items():
                    if value == '':
                        record[key] = None
            return records
        except Exception as e:
            st.error(f"Error fetching records: {e}")
            return []
    
    def _add_record(self, record):
        """Add a new record to the worksheet"""
        if self.is_mock:
            # Generate a mock ID
            record['ID'] = len(self.mock_data) + 1
            self.mock_data.append(record)
            return True
        
        try:
            # Convert record to list format for Google Sheets
            values = [
                record.get('ID', ''),
                record.get('Case Number', ''),
                record.get('Case Title', ''),
                record.get('Case Type', ''),
                record.get('Location', ''),
                record.get('Company Name', ''),
                str(record.get('Upcoming Date', '')),
                record.get('Previous Dates', ''),
                record.get('Stage', ''),
                record.get('Remarks', ''),
                record.get('Status', ''),
                record.get('Claimant Advocate Name', ''),
                record.get('Claimant Advocate Mobile Number', '')
            ]
            
            self.worksheet.append_row(values)
            return True
        except Exception as e:
            st.error(f"Error adding record: {e}")
            return False
    
    def _update_record(self, record_id, record):
        """Update an existing record"""
        if self.is_mock:
            for i, existing_record in enumerate(self.mock_data):
                if existing_record.get('ID') == record_id:
                    record['ID'] = record_id
                    self.mock_data[i] = record
                    return True
            return False
        
        try:
            # Find the row with the matching ID
            records = self.worksheet.get_all_records()
            for i, existing_record in enumerate(records, start=2):  # Start from row 2 (skip header)
                if existing_record.get('ID') == record_id:
                    # Update the row
                    values = [
                        record.get('ID', ''),
                        record.get('Case Number', ''),
                        record.get('Case Title', ''),
                        record.get('Case Type', ''),
                        record.get('Location', ''),
                        record.get('Company Name', ''),
                        str(record.get('Upcoming Date', '')),
                        record.get('Previous Dates', ''),
                        record.get('Stage', ''),
                        record.get('Remarks', ''),
                        record.get('Status', ''),
                        record.get('Claimant Advocate Name', ''),
                        record.get('Claimant Advocate Mobile Number', '')
                    ]
                    
                    self.worksheet.update(f'A{i}:M{i}', [values])
                    return True
            return False
        except Exception as e:
            st.error(f"Error updating record: {e}")
            return False
    
    def add_case(self, case_data):
        """Add a new case"""
        # Generate ID for new case
        all_records = self._get_all_records()
        new_id = max([r.get('ID', 0) for r in all_records], default=0) + 1
        case_data['ID'] = new_id
        
        return self._add_record(case_data)
    
    def case_number_exists(self, case_number, location):
        """Check if case number exists for the given location"""
        records = self._get_all_records()
        search_value = str(case_number).strip()
        for record in records:
            if (str(record.get('Case Number', '')).strip() == search_value and 
                record.get('Location') == location):
                return True
        return False
    
    def search_by_case_number(self, case_number):
        """Search cases by case number"""
        records = self._get_all_records()
        # Convert both to strings for comparison to handle int/string mismatches
        search_value = str(case_number).strip()
        return [r for r in records if str(r.get('Case Number', '')).strip() == search_value]
    
    def search_by_case_title(self, case_title):
        """Search cases by case title (partial match)"""
        records = self._get_all_records()
        return [r for r in records if case_title.lower() in r.get('Case Title', '').lower()]
    
    def get_cases_by_date(self, selected_date):
        """Get cases for a specific date"""
        records = self._get_all_records()
        target_date = str(selected_date)
        return [r for r in records if str(r.get('Upcoming Date', '')) == target_date]
    
    def get_todays_case_list(self):
        """Get today's cases"""
        today = date.today()
        return self.get_cases_by_date(today)
    
    def get_pending_cases(self):
        """Get pending cases (upcoming_date <= today)"""
        records = self._get_all_records()
        today = str(date.today())
        return [r for r in records if str(r.get('Upcoming Date', '')) <= today]
    
    def search_by_company_name(self, company_name):
        """Search cases by company name"""
        records = self._get_all_records()
        return [r for r in records if company_name.lower() in r.get('Company Name', '').lower()]
    
    def get_case_by_number_or_title(self, search_query):
        """Get case by number or title"""
        records = self._get_all_records()
        search_value = str(search_query).strip()
        for record in records:
            if (str(record.get('Case Number', '')).strip() == search_value or 
                search_value.lower() in record.get('Case Title', '').lower()):
                return record
        return None
    
    def update_case_data(self, case_id, upcoming_date):
        """Update case upcoming date and previous dates"""
        records = self._get_all_records()
        for record in records:
            if record.get('ID') == case_id:
                current_upcoming_date = record.get('Upcoming Date')
                previous_dates = record.get('Previous Dates', '')
                
                # Convert previous_dates to list
                if previous_dates:
                    previous_dates_list = previous_dates.split(", ")
                else:
                    previous_dates_list = []
                
                # Add current upcoming date to previous dates if not already there
                if str(current_upcoming_date) not in previous_dates_list:
                    previous_dates_list.append(str(current_upcoming_date))
                
                # Check if new date is already in previous dates
                if str(upcoming_date) in previous_dates_list:
                    return "The upcoming date is already present in the previous dates list."
                
                # Update the record
                record['Upcoming Date'] = str(upcoming_date)
                record['Previous Dates'] = ", ".join(previous_dates_list)
                
                return self._update_record(case_id, record)
        
        return "Case not found."
    
    def update_case(self, case_id, case_data):
        """Update case with new data"""
        case_data['ID'] = case_id
        return self._update_record(case_id, case_data)
