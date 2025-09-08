# Google Sheets Setup Guide

## ✅ Application Status
Your **Case Management System** is now successfully running with **Google Sheets integration** instead of a PostgreSQL database!

**🌐 Access your application at: http://localhost:8501**

## 🚀 What's Changed

### ✅ **No Database Required**
- Removed PostgreSQL dependency
- All data now stored in Google Sheets
- Works with mock data when Google Sheets is not configured

### ✅ **New Features**
- **Mock Data Mode**: Application works immediately with sample data
- **Google Sheets Integration**: Real-time data sync with Google Sheets
- **Same UI**: All existing features work exactly the same

## 📋 Setup Options

### Option 1: Use Mock Data (Immediate Use)
The application is already working with mock data! You can:
- Add, search, and update cases
- All data is stored in memory during the session
- Perfect for testing and demonstration

### Option 2: Connect to Google Sheets (Production Use)

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API

#### Step 2: Create Service Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it "advocate-diary-sheets"
4. Click "Create and Continue"
5. Skip role assignment for now
6. Click "Done"

#### Step 3: Generate Credentials
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose "JSON" format
5. Download the JSON file

#### Step 4: Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it "Case Management System"
4. Create a worksheet named "case_records"
5. Add headers in row 1:
   ```
   ID | Case Number | Case Title | Case Type | Location | Company Name | Upcoming Date | Previous Dates | Stage | Remarks | Status | Claimant Advocate Name | Claimant Advocate Mobile Number
   ```

#### Step 5: Share Sheet with Service Account
1. Click "Share" on your Google Sheet
2. Add the service account email (from JSON file)
3. Give "Editor" permissions
4. Copy the spreadsheet ID from the URL

#### Step 6: Configure Application
Replace the placeholder values in `config.json`:

```json
{
    "google_sheets": {
        "spreadsheet_id": "YOUR_SPREADSHEET_ID_HERE",
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
}
```

## 🔧 Alternative: Streamlit Secrets (Recommended for Production)

For better security, use Streamlit secrets instead of config.json:

1. Create `.streamlit/secrets.toml` file:
```toml
[google_sheets]
spreadsheet_id = "YOUR_SPREADSHEET_ID_HERE"
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

## 🎯 Features Available

### ✅ **All Original Features Work**
- ➕ Add New Case
- 🔍 Search Case (by number or title)
- 📅 Today's Case List
- 📆 Cases by Date
- ⏳ Pending Cases
- 🏢 Cases By Company Name
- ✍️ Update Case

### ✅ **New Benefits**
- **No Database Setup**: No PostgreSQL installation required
- **Cloud Storage**: Data stored in Google Sheets
- **Real-time Sync**: Multiple users can access the same data
- **Easy Backup**: Google Sheets handles data backup
- **Access Control**: Use Google's sharing permissions

## 🚨 Troubleshooting

### If you see "No secrets found" error:
- The app is trying to use Google Sheets but can't find credentials
- It will automatically fall back to mock data mode
- This is normal and expected behavior

### If you want to use real Google Sheets:
- Follow the setup steps above
- Make sure the service account has access to your sheet
- Verify the spreadsheet ID is correct

## 📊 Data Format

The application expects this column structure in your Google Sheet:
1. **ID** - Auto-generated unique identifier
2. **Case Number** - Case reference number
3. **Case Title** - Description of the case
4. **Case Type** - MACT, WCC, DCF, PLA
5. **Location** - Court location
6. **Company Name** - Insurance company
7. **Upcoming Date** - Next hearing date
8. **Previous Dates** - Comma-separated list of past dates
9. **Stage** - Current stage of the case
10. **Remarks** - Additional notes
11. **Status** - OPEN, COMPROMISED, DD, AWARD
12. **Claimant Advocate Name** - Lawyer's name
13. **Claimant Advocate Mobile Number** - Contact number

## 🎉 You're All Set!

Your Case Management System is now running with Google Sheets integration. You can start using it immediately with mock data, or set up Google Sheets for persistent storage.

**Access your application at: http://localhost:8501**
