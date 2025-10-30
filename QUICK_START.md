# 🚀 Quick Start Guide

## Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python setup.py
```

This will:
1. ✓ Install all dependencies
2. ✓ Create sample volunteer data (15 volunteers)
3. ✓ Sync data to SQLite database

Then start the application:

```bash
python app.py
```

Open your browser to: **http://localhost:5000**

---

## Option 2: Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Sample Data
```bash
python create_sample_data.py
```

This creates `volunteers_data.xlsx` with 15 sample volunteers.

### Step 3: Sync to Database
```bash
python excel_sync.py
```

This imports the Excel data into `volunteer_management.db`.

### Step 4: Run the Application
```bash
python app.py
```

Open: **http://localhost:5000**

---

## 🎯 How to Use

1. **Enter Job Description**: In the text area, describe the position and required skills

   Example:
   ```
   We need a volunteer web developer with Python and Django experience. 
   Knowledge of REST APIs and frontend technologies like React is preferred.
   ```

2. **Set Maximum Results**: Choose how many volunteers to shortlist (default: 10)

3. **Click "Find Matching Volunteers"**: The AI will analyze and match volunteers

4. **View Results**: See shortlisted volunteers with:
   - Match scores (percentage)
   - Contact information
   - Skills and experience
   - Matching skills highlighted

5. **Clear Results**: Click "Clear All" to reset and start fresh

---

## 📊 Using Your Own Data

### From Excel File

1. Create an Excel file with these columns:
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

2. Update `excel_sync.py` with your file path:
   ```python
   excel_file = "your_volunteers_data.xlsx"
   ```

3. Run the sync:
   ```bash
   python excel_sync.py
   ```

### Manual Database Entry

You can also add volunteers programmatically:

```python
from database import Database

db = Database()

volunteer_data = {
    'name': 'Jane Doe',
    'email': 'jane@example.com',
    'phone': '+1-555-0000',
    'skills': 'Python, Machine Learning, TensorFlow',
    'experience': '4 years data science',
    'education': 'Master of Data Science',
    'availability': 'Weekends',
    'languages': 'English, Spanish',
    'certifications': 'TensorFlow Developer Certificate',
    'interests': 'AI, education, research'
}

db.insert_volunteer(volunteer_data)
```

---

## 🔧 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Database locked error
Close any open database connections and restart the app.

### No volunteers found
Make sure you ran `python excel_sync.py` to populate the database.

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

---

## 🌟 Tips for Best Results

1. **Write detailed job descriptions**: Include specific skills, technologies, and requirements
2. **Use technical terms**: The AI matches based on keywords like "Python", "React", "leadership"
3. **Adjust max results**: Increase to see more candidates, decrease for only top matches
4. **Review match scores**: Higher percentages indicate better matches
5. **Check matching skills**: Shows which skills overlap with job requirements

---

## 📞 Need Help?

Check the full README.md for:
- Architecture details
- API documentation
- Customization options
- Advanced features

Happy volunteering! 🎉

