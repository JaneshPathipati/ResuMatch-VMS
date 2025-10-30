# 🔗 Google Sheets Integration Setup Guide

This guide will help you connect your Google Sheet to automatically sync volunteer data to the database.

## 📋 Prerequisites

Your Google Sheet should have these columns:
- Name
- Email
- Phone
- Skills
- Experience
- Education
- Availability
- Languages
- Certifications
- Interests

---

## 🚀 Setup Steps

### Step 1: Install Required Packages

```bash
pip install gspread google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 2: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Name it "Volunteer Management System" or similar

### Step 3: Enable Google Sheets API

1. In Google Cloud Console, go to **"APIs & Services" → "Library"**
2. Search for **"Google Sheets API"**
3. Click **"Enable"**
4. Also enable **"Google Drive API"**

### Step 4: Create Service Account

1. Go to **"APIs & Services" → "Credentials"**
2. Click **"Create Credentials" → "Service Account"**
3. Enter name: "volunteer-sync-service"
4. Click **"Create and Continue"**
5. Skip optional steps, click **"Done"**

### Step 5: Generate Credentials JSON

1. Click on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key" → "Create new key"**
4. Choose **JSON** format
5. Click **"Create"**
6. Save the downloaded JSON file as `credentials.json` in your project folder

### Step 6: Share Google Sheet with Service Account

1. Open the downloaded `credentials.json` file
2. Find the `"client_email"` field (looks like: `xxxx@xxxx.iam.gserviceaccount.com`)
3. Copy this email address
4. Open your Google Sheet
5. Click **"Share"** button
6. Paste the service account email
7. Give it **"Viewer"** or **"Editor"** access
8. Click **"Send"**

---

## ✅ You're Ready!

Your setup is complete. Now you can sync data from your Google Sheet!

---

## 🔄 How to Sync

### Option 1: One-Time Sync

```bash
python google_sheets_sync.py
```

Choose option 1, then enter your Google Sheet URL or ID.

### Option 2: Auto-Sync (Recommended)

```bash
python google_sheets_sync.py
```

Choose option 2 to sync automatically every few minutes.

### Option 3: Command Line Sync

```bash
python -c "from google_sheets_sync import GoogleSheetSync; sync = GoogleSheetSync(); sync.sync_from_sheet('YOUR_SHEET_URL')"
```

---

## 📝 Finding Your Sheet URL/ID

Your Google Sheet URL looks like:
```
https://docs.google.com/spreadsheets/d/1ABC123xyz456/edit
```

You can use either:
- **Full URL**: `https://docs.google.com/spreadsheets/d/1ABC123xyz456/edit`
- **Sheet ID only**: `1ABC123xyz456` (the part between `/d/` and `/edit`)

---

## 🔧 Configuration Options

### Sync Interval

Change how often auto-sync runs:

```python
# Sync every 5 minutes (300 seconds)
syncer.auto_sync(sheet_url, interval_seconds=300)

# Sync every 1 minute
syncer.auto_sync(sheet_url, interval_seconds=60)

# Sync every 30 minutes
syncer.auto_sync(sheet_url, interval_seconds=1800)
```

### Worksheet Name

If your data is in a different worksheet:

```python
syncer.sync_from_sheet(sheet_url, worksheet_name='Form Responses 1')
```

---

## 🎯 Google Form Integration

If you're collecting data via Google Forms:

1. Google Forms automatically creates a responses sheet
2. The sheet is usually named **"Form Responses 1"**
3. Use this as your worksheet name:

```bash
python google_sheets_sync.py
# Choose option 1 or 2
# Enter worksheet name: Form Responses 1
```

---

## 🔒 Security Notes

- **Never commit** `credentials.json` to Git (it's already in `.gitignore`)
- Keep your credentials file secure
- Only share your Google Sheet with the service account email
- Use "Viewer" access for read-only sync (recommended)

---

## 🐛 Troubleshooting

### Error: "Credentials file not found"
- Make sure `credentials.json` is in your project folder
- Check the file name is exactly `credentials.json`

### Error: "Spreadsheet not found"
- Verify you shared the sheet with the service account email
- Check the Sheet URL/ID is correct
- Make sure the sheet isn't deleted

### Error: "Worksheet not found"
- Check the worksheet name (case-sensitive)
- Default is "Sheet1"
- For Google Forms, try "Form Responses 1"

### Duplicate emails skipped
- The database uses email as a unique identifier
- Duplicate emails won't be inserted twice
- This is normal behavior

---

## 📊 Example Google Sheet Format

| Name | Email | Phone | Skills | Experience | Education | Availability | Languages | Certifications | Interests |
|------|-------|-------|--------|------------|-----------|--------------|-----------|----------------|-----------|
| John Doe | john@email.com | +1-555-0100 | Python, Django | 3 years web dev | BS Computer Science | Weekends | English, Spanish | AWS Certified | Web development |
| Jane Smith | jane@email.com | +1-555-0101 | React, JavaScript | 2 years frontend | BS Software Eng | Evenings | English | None | UI/UX Design |

---

## 🔄 Automated Sync Options

### Option A: Run as Background Service

On Windows, create a scheduled task:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup" or "Daily")
4. Action: Start a program
5. Program: `python`
6. Arguments: `path\to\google_sheets_sync.py`

### Option B: Keep Terminal Open

Simply run:
```bash
python google_sheets_sync.py
```
Choose auto-sync and let it run continuously.

### Option C: Webhook (Advanced)

For real-time sync when forms are submitted, consider setting up Google Apps Script webhook.

---

## 📞 Need Help?

If you encounter issues:
1. Check `credentials.json` is in the correct location
2. Verify Google Sheet is shared with service account
3. Make sure column names match exactly
4. Check for typos in worksheet name

---

## ✨ Summary

1. ✅ Install packages: `pip install gspread google-auth`
2. ✅ Create Google Cloud project
3. ✅ Enable Google Sheets API
4. ✅ Create service account
5. ✅ Download `credentials.json`
6. ✅ Share your sheet with service account email
7. ✅ Run: `python google_sheets_sync.py`

Done! Your Google Sheet will now sync to the database automatically! 🎉
