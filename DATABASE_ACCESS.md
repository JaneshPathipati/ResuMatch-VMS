# 🗄️ Database Access Guide

Your volunteer management database is stored in: **`volunteer_management.db`**

## 📊 Quick Access Methods

### Method 1: Database Viewer Script (Recommended)
Run the interactive database viewer:

```bash
python view_database.py
```

**Features:**
- ✅ View all volunteers
- ✅ View shortlisted volunteers  
- ✅ Database statistics
- ✅ Search volunteers by keyword
- ✅ Export data to JSON

---

### Method 2: SQL Query Tool
Run custom SQL queries:

```bash
python sql_query.py
```

**Features:**
- ✅ Predefined useful queries
- ✅ Custom SQL queries
- ✅ View table schemas
- ✅ Direct database access

---

### Method 3: SQLite Browser (GUI Tool)
Download and install **DB Browser for SQLite**:
- Download: https://sqlitebrowser.org/dl/
- Open: `volunteer_management.db`
- Browse, edit, and query visually

---

### Method 4: Command Line (SQLite)

```bash
# Open database in SQLite command line
sqlite3 volunteer_management.db

# Then run queries:
.tables                          # Show all tables
.schema volunteers              # Show table structure
SELECT * FROM volunteers;       # View all volunteers
SELECT * FROM shortlisted_volunteers;  # View shortlisted
.quit                           # Exit
```

---

### Method 5: Python Script

```python
from database import Database

# Initialize database connection
db = Database()

# Get all volunteers
volunteers = db.get_all_volunteers()
for v in volunteers:
    print(f"{v['name']} - {v['email']}")

# Get shortlisted volunteers
shortlisted = db.get_shortlisted_volunteers()
for s in shortlisted:
    print(f"{s['name']} - Score: {s['match_score']}%")
```

---

## 📋 Database Schema

### Table: `volunteers`
- `id` - Primary key
- `name` - Volunteer name
- `email` - Email (unique)
- `phone` - Phone number
- `skills` - Skills and technologies
- `experience` - Work experience
- `education` - Educational background
- `availability` - Time availability
- `languages` - Languages spoken
- `certifications` - Professional certifications
- `interests` - Areas of interest
- `created_at` - Timestamp

### Table: `shortlisted_volunteers`
- `id` - Primary key
- `volunteer_id` - Foreign key to volunteers
- `job_description` - Job description used
- `match_score` - Match score (0-100)
- `matching_skills` - JSON array of matching skills
- `shortlisted_at` - Timestamp

### Table: `job_postings`
- `id` - Primary key
- `title` - Job title
- `description` - Job description
- `required_skills` - Required skills
- `created_at` - Timestamp

---

## 🔍 Useful SQL Queries

### View all volunteers with skills
```sql
SELECT id, name, email, skills, experience 
FROM volunteers 
ORDER BY created_at DESC;
```

### Find volunteers with specific skills
```sql
SELECT name, email, skills 
FROM volunteers 
WHERE skills LIKE '%Python%';
```

### View shortlisted volunteers with match scores
```sql
SELECT v.name, v.email, v.skills, s.match_score, s.matching_skills
FROM shortlisted_volunteers s
JOIN volunteers v ON s.volunteer_id = v.id
ORDER BY s.match_score DESC;
```

### Count volunteers by availability
```sql
SELECT availability, COUNT(*) as count
FROM volunteers
GROUP BY availability;
```

### Get top 5 matches
```sql
SELECT v.name, v.email, s.match_score
FROM shortlisted_volunteers s
JOIN volunteers v ON s.volunteer_id = v.id
ORDER BY s.match_score DESC
LIMIT 5;
```

---

## 📤 Export Data

### Export to JSON
```bash
python view_database.py
# Choose option 5: Export Data to JSON
```

This creates:
- `volunteers_export.json` - All volunteers
- `shortlisted_export.json` - All shortlisted volunteers

### Export to CSV (using SQLite)
```bash
sqlite3 volunteer_management.db
.headers on
.mode csv
.output volunteers.csv
SELECT * FROM volunteers;
.output shortlisted.csv
SELECT * FROM shortlisted_volunteers;
.quit
```

---

## 🛠️ Database Maintenance

### Clear shortlisted volunteers
```python
from database import Database
db = Database()
db.clear_shortlisted_volunteers()
```

### Add a new volunteer programmatically
```python
from database import Database

db = Database()

volunteer = {
    'name': 'New Volunteer',
    'email': 'newvol@example.com',
    'phone': '+1-555-0000',
    'skills': 'Python, JavaScript',
    'experience': '2 years',
    'education': 'Bachelor of CS',
    'availability': 'Weekends',
    'languages': 'English',
    'certifications': 'None',
    'interests': 'Web development'
}

db.insert_volunteer(volunteer)
```

### Backup database
```bash
# Simple file copy
copy volunteer_management.db volunteer_management_backup.db

# Or using SQLite
sqlite3 volunteer_management.db ".backup volunteer_management_backup.db"
```

---

## 📊 Database Location

The database file is located at:
```
C:\Users\pathi\OneDrive\Desktop\New folder\volunteer_management.db
```

You can:
- Copy it to another location
- Open it with any SQLite tool
- Back it up regularly
- Share it with others

---

## 🔗 API Access

You can also access the database through the web API:

```bash
# Get all volunteers
curl http://localhost:5000/api/volunteers

# Get shortlisted volunteers
curl http://localhost:5000/api/shortlisted

# Get statistics
curl http://localhost:5000/api/stats
```

---

Need help? Run the database viewer for an interactive experience:
```bash
python view_database.py
```
