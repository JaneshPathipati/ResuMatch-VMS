# 🚀 How to Run the Volunteer Management System

## ✅ All Dependencies Installed Successfully!

All required Python packages are installed and verified:
- ✅ Flask
- ✅ pandas
- ✅ scikit-learn
- ✅ gspread (Google Sheets)
- ✅ numpy, openpyxl, etc.

---

## 🎯 Quick Start (Choose One Method)

### **Method 1: Double-Click Startup File** (Easiest)
Simply double-click: **`START_APP.bat`**

### **Method 2: Command Line**
Open PowerShell or Command Prompt in this folder and run:
```bash
python app.py
```

### **Method 3: PowerShell Script**
```bash
.\START_APP.ps1
```

---

## 📋 What Happens When You Start

1. Database initializes (volunteer_management.db)
2. Flask server starts on port 5000
3. You'll see:
   ```
   ============================================================
   Volunteer Management System Starting...
   ============================================================
   Initializing database...
   Database ready!
   Server starting at http://localhost:5000
   ============================================================
   ```

4. **Open your browser** to: **http://localhost:5000**

---

## 🌐 Using the Web Interface

1. **Open**: http://localhost:5000
2. **Enter job description** in the text box, e.g.:
   ```
   Looking for volunteer with PHP and MySQL experience.
   WordPress knowledge is a plus. Testing and QA skills preferred.
   ```
3. **Click**: "Find Matching Volunteers"
4. **View**: AI-matched volunteers with scores and matching skills
5. **Result**: Shortlisted volunteers automatically saved to database

---

## 🔄 Other Useful Commands

### **Sync Google Sheet** (Manual)
```bash
python auto_sync_geeta.py
```

### **Auto-Sync** (Every 5 minutes)
```bash
python auto_sync_geeta.py --continuous
```

### **View Database**
```bash
python show_data.py
```

### **Test System**
```bash
python test_system.py
```

---

## 🐛 Troubleshooting

### **"Module not found" Error**
If you still get module errors, run:
```bash
python -m pip install --user Flask flask-cors pandas openpyxl scikit-learn numpy gspread google-auth
```

### **Port 5000 Already in Use**
Edit `app.py` line 175:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### **Database Error**
Delete `volunteer_management.db` and restart - it will recreate automatically.

---

## 📊 Your Current Setup

- **Database**: 120 volunteers from Google Sheet
- **Location**: `volunteer_management.db`
- **Google Sheet**: Synced and connected
- **Credentials**: `credentials.json` configured

---

## ✨ Complete Workflow

```
Google Form 
    → Google Sheet
    → Auto-Sync (python auto_sync_geeta.py --continuous)
    → SQLite Database (120 volunteers)
    → Web Interface (http://localhost:5000)
    → AI Matching
    → Shortlisted Volunteers (saved to database)
    → Display Results
```

---

## 🎉 You're All Set!

Just run:
```bash
python app.py
```

Then open: **http://localhost:5000**

Happy volunteering! 🚀

