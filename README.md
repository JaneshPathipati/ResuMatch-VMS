# 🎯 Volunteer Management System

An AI-powered volunteer management application that uses resume parsing and intelligent matching to shortlist volunteers based on job descriptions.

## 📋 Features

- **Excel Data Sync**: Import volunteer data from Excel files into SQL database
- **AI-Powered Matching**: Uses TF-IDF and cosine similarity to match volunteers with job requirements
- **Modern Frontend**: Clean, responsive UI for HR managers to enter job descriptions
- **Shortlisting System**: Automatically shortlist and rank volunteers based on match scores
- **Database Storage**: All data and shortlisted candidates stored in SQL database
- **Real-time Stats**: View total volunteers and shortlisted count at a glance

## 🏗️ Architecture

```
├── app.py                    # Flask backend API
├── database.py               # Database models and operations
├── resume_matcher.py         # AI matching engine
├── excel_sync.py             # Excel to database sync script
├── create_sample_data.py     # Generate sample volunteer data
├── templates/
│   └── index.html           # Frontend interface
├── volunteers_data.xlsx      # Sample volunteer data (generated)
└── volunteer_management.db   # SQLite database (generated)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Sample Data

```bash
python create_sample_data.py
```

This generates `volunteers_data.xlsx` with 15 sample volunteers.

### 3. Sync Data to Database

```bash
python excel_sync.py
```

This imports the Excel data into the SQL database.

### 4. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## 📊 Database Schema

### Volunteers Table
- `id`: Primary key
- `name`: Volunteer name
- `email`: Email address (unique)
- `phone`: Phone number
- `skills`: Skills and technologies
- `experience`: Work experience
- `education`: Educational background
- `availability`: Time availability
- `languages`: Languages spoken
- `certifications`: Professional certifications
- `interests`: Areas of interest
- `created_at`: Timestamp

### Shortlisted Volunteers Table
- `id`: Primary key
- `volunteer_id`: Foreign key to volunteers
- `job_description`: Job description used for matching
- `match_score`: Matching score (0-100)
- `matching_skills`: JSON array of matching skills
- `shortlisted_at`: Timestamp

## 🎨 How to Use

1. **View Dashboard**: Open http://localhost:5000 in your browser
2. **Enter Job Description**: Fill in the job requirements, skills needed, etc.
3. **Set Parameters**: Adjust maximum results (default: 10)
4. **Find Matches**: Click "Find Matching Volunteers"
5. **Review Results**: View shortlisted volunteers with match scores and matching skills
6. **Clear Results**: Use "Clear All" button to reset shortlisted volunteers

## 📝 Example Job Descriptions

### Web Developer Position
```
We are looking for a volunteer web developer with strong Python and JavaScript skills. 
Experience with Django or Flask frameworks is required. The ideal candidate should have 
knowledge of frontend technologies like React, and be comfortable with REST APIs and databases.
```

### Data Analyst Position
```
Seeking a data analyst volunteer with expertise in Python, R, and statistical analysis. 
Experience with machine learning, data visualization, and SQL is essential. The candidate 
should be able to extract insights from complex datasets.
```

### Mobile Developer Position
```
Looking for a mobile app developer experienced in Flutter or React Native. Knowledge of 
both iOS and Android platforms is preferred. Experience with Firebase and modern mobile 
development practices is a plus.
```

## 🔧 API Endpoints

- `GET /` - Main frontend page
- `GET /api/volunteers` - Get all volunteers
- `POST /api/shortlist` - Shortlist volunteers based on job description
- `GET /api/shortlisted` - Get all shortlisted volunteers
- `DELETE /api/shortlisted/clear` - Clear shortlisted volunteers
- `GET /api/stats` - Get database statistics

## 📦 Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **ML/AI**: scikit-learn (TF-IDF, Cosine Similarity)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Processing**: Pandas, NumPy

## 🔄 Resume Matching Algorithm

The system uses a sophisticated matching algorithm:

1. **Text Preprocessing**: Clean and normalize job descriptions and volunteer profiles
2. **Feature Extraction**: Extract skills, keywords, and experience from both job description and volunteer data
3. **TF-IDF Vectorization**: Convert text to numerical vectors using Term Frequency-Inverse Document Frequency
4. **Cosine Similarity**: Calculate similarity scores between job requirements and volunteer profiles
5. **Skill Matching**: Identify specific matching skills between job and volunteer
6. **Ranking**: Sort candidates by match score and return top N results

## 🎯 Customization

### Change Database
Edit `database.py` to use MySQL or PostgreSQL instead of SQLite:

```python
# For MySQL
import mysql.connector
conn = mysql.connector.connect(host='localhost', user='root', password='password', database='volunteers')
```

### Adjust Matching Algorithm
Modify `resume_matcher.py` to customize:
- Minimum match score threshold
- Number of results returned
- Weighting of different skills
- Keyword extraction logic

### Customize Frontend
Edit `templates/index.html` to change:
- Colors and styling
- Layout and components
- Form fields
- Display format

## 📈 Future Enhancements

- [ ] Google Forms integration for live data sync
- [ ] Advanced filtering (availability, location, etc.)
- [ ] Export shortlisted candidates to PDF/Excel
- [ ] Email notifications to shortlisted volunteers
- [ ] Multi-tenant support for different organizations
- [ ] Advanced analytics and reporting
- [ ] Interview scheduling integration

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📄 License

This project is open source and available under the MIT License.

## 👥 Support

For questions or issues, please create an issue in the repository.

---

**Made with ❤️ for efficient volunteer management**

