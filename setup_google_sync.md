# 🚀 Quick Setup for Geeta Sevi Google Sheet Sync

## Your Google Sheet
**URL:** https://docs.google.com/spreadsheets/d/16_SnaTYS0O5qvTBesXB5jEe3V0hk6nN2D8mvNWEBTDE/edit?usp=sharing

---

## ⚡ Quick Start (3 Steps)

### Step 1: Install Google Packages
```bash
pip install gspread google-auth google-auth-oauthlib google-auth-httplib2
```

### Step 2: Set Up Google API Access

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Create a new project (name it "Volunteer Sync" or similar)

2. **Enable Google Sheets API**
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
   - Also enable "Google Drive API"

3. **Create Service Account**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Name: "volunteer-sync"
   - Click "Create and Continue", then "Done"

4. **Generate Credentials File**
   - Click on the service account you created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Choose "JSON"
   - Save the file as `credentials.json` in your project folder
     (`C:\Users\pathi\OneDrive\Desktop\New folder\credentials.json`)

5. **Share Google Sheet**
   - Open `credentials.json` in notepad
   - Find the line with `"client_email"`: It looks like: `xxxx@xxxx.iam.gserviceaccount.com`
   - Copy this email
   - Open your Google Sheet: https://docs.google.com/spreadsheets/d/16_SnaTYS0O5qvTBesXB5jEe3V0hk6nN2D8mvNWEBTDE/edit
   - Click "Share" button (top right)
   - Paste the service account email
   - Give it "Viewer" access
   - Click "Send"

### Step 3: Run the Sync
```bash
python sync_geeta_sheet.py
```

Choose option 1 for one-time sync, or option 2 for auto-sync!

---

## 🎯 What Gets Synced

The script maps your sheet columns to our database:

| Google Sheet Column | Database Field | Notes |
|---------------------|----------------|-------|
| Name | name | Primary identifier |
| Email address | email | Unique key |
| Mobile Number | phone | Contact |
| Expertise Areas | skills | All expertise combined |
| Contribution Area | experience | What they want to contribute |
| Association Duration | availability | How long they've been associated |
| LinkedIn Profile | certifications | Professional link |
| (Auto-filled) | interests | Set to "IT volunteer work" |

---

## 🔄 Auto-Sync Features

### One-Time Sync
```bash
python sync_geeta_sheet.py
# Choose option 1
```
Syncs once and exits.

### Continuous Auto-Sync (Recommended)
```bash
python sync_geeta_sheet.py
# Choose option 2
```
Automatically syncs every 5 minutes. New Google Form submissions will appear in your database!

### Custom Interval
```bash
python sync_geeta_sheet.py
# Choose option 3
# Enter interval (e.g., 60 for every minute)
```

---

## 📊 Expected Results

After syncing, you'll see volunteers with:
- **Skills**: PHP + MySQL, Wordpress, AI Programming, Digital Marketing, etc.
- **Experience**: Their contribution areas
- **Availability**: Since when they're associated with Geeta Parivar
- **Certifications**: LinkedIn profiles

All volunteers will be available for AI matching in the web interface!

---

## ✅ Verification

After sync completes, check the data:
```bash
python show_data.py
```

Or view in web interface:
- Open http://localhost:5000
- Check the "Total Volunteers" count
- Try searching with a job description

---

## 🐛 Troubleshooting

### "Credentials file not found"
- Make sure `credentials.json` is in: `C:\Users\pathi\OneDrive\Desktop\New folder\`
- Check the filename is exactly `credentials.json`

### "Spreadsheet not found"
- Verify you shared the sheet with the service account email
- Make sure you clicked "Send" after adding the email

### "Worksheet not found"
- The script tries "Form responses 1" first
- Edit `sync_geeta_sheet.py` line 11 if your worksheet has a different name

### No data synced
- Check if your sheet has data rows (not just headers)
- Verify email column has valid emails

---

## 🎉 You're All Set!

Once setup is complete:
1. New Google Form submissions → Google Sheet
2. Auto-sync script → SQLite Database
3. Web interface → AI Matching → Shortlisted Volunteers

Complete end-to-end automation! 🚀

