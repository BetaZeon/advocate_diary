from .google_sheets import GoogleSheetsService

def get_connection():
    """Get Google Sheets service connection"""
    return GoogleSheetsService()
