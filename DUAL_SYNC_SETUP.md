# Dual Google Sheets Auto-Sync Setup

## Overview
You now have **TWO** Google Sheets syncing to your database:

1. **Geeta Sevi IT Interest Areas**  
   URL: https://docs.google.com/spreadsheets/d/16_SnaTYS0O5qvTBesXB5jEe3V0hk6nN2D8mvNWEBTDE/edit?usp=sharing

2. **VMS Volunteers Data**  
   URL: https://docs.google.com/spreadsheets/d/1qSqLPy5Q6mLA6Q1nUTKtlKx1kLAagFsrPCZ5x8vKjW8/edit?usp=sharing

## Setup Steps

### Step 1: Share the Second Sheet with Service Account

1. Open your `credentials.json` file
2. Find the `client_email` (looks like: `something@project-id.iam.gserviceaccount.com`)
3. Open the **VMS Volunteers sheet**: https://docs.google.com/spreadsheets/d/1qSqLPy5Q6mLA6Q1nUTKtlKx1kLAagFsrPCZ5x8vKjW8/edit?usp=sharing
4. Click **Share** button
5. Paste the service account email
6. Set permission to **Viewer**
7. Click **Send**

### Step 2: Run the Sync

You have three options:

#### Option A: Auto-Sync Both Sheets (RECOMMENDED)
```bash
RUN_DUAL_SYNC.bat
```
This will continuously sync **both sheets** every 5 minutes.

#### Option B: Sync Individual Sheets

**Geeta Sevi Sheet Only:**
```bash
python sync_geeta_sheet.py
```

**VMS Volunteers Sheet Only:**
```bash
python sync_vms_volunteers.py
```

#### Option C: One-Time Sync Both Sheets
```bash
python auto_sync_both_sheets.py
```
Choose option 1 for a one-time sync.

## How It Works

- **No Duplicates**: Email is unique - if a volunteer exists, they won't be added again
- **Serial IDs**: New volunteers get sequential IDs automatically (continuing from last ID)
- **Continuous Sync**: New entries in either sheet are automatically added to database
- **Column Mapping**: Each sheet's columns are mapped to the database schema

## Database Schema

Both sheets sync to the same `volunteers` table:

- `name` - Volunteer's full name
- `email` - Email address (unique)
- `phone` - Phone number
- `skills` - Skills/expertise/profession
- `experience` - Work experience
- `education` - Educational qualifications
- `availability` - Availability information
- `languages` - Languages known
- `certifications` - LinkedIn/certifications
- `interests` - Interests/areas of interest

## Checking Synced Data

View all volunteers:
```bash
python view_database.py
```

Run SQL queries:
```bash
python sql_query.py
```

## Troubleshooting

### "Spreadsheet not found"
- Make sure you shared the sheet with your service account email
- Check the email in `credentials.json` -> `client_email`

### "Worksheet not found"
- The script will auto-detect the first worksheet
- Check available worksheet names in the error message

### Duplicates not syncing
- This is correct! Email is unique - same email won't be added twice
- Update existing records by deleting them first

## Files Created

- `sync_geeta_sheet.py` - Sync script for Sheet 1
- `sync_vms_volunteers.py` - Sync script for Sheet 2
- `auto_sync_both_sheets.py` - Master sync script for both sheets
- `RUN_DUAL_SYNC.bat` - Quick launcher for dual auto-sync

## Next Steps

1. Share the VMS Volunteers sheet with your service account
2. Run `RUN_DUAL_SYNC.bat`
3. Let it run in the background
4. Both sheets will stay synced automatically!

---

**Note**: Keep the sync script running to maintain continuous sync. If you close it, just run `RUN_DUAL_SYNC.bat` again.

