# 🎯 ResuMatch VMS
**AI-Powered Volunteer Management System**

An intelligent volunteer recruitment platform that uses AI-powered resume parsing and hybrid matching algorithms to shortlist the best volunteers for your organization.

## ✨ Features

- 📄 **Resume Upload**: Upload PDF/DOCX resumes with automatic data extraction
- 🤖 **AI Keyword Extraction**: GPT-4 powered job description analysis
- 🎯 **Hybrid Matching**: TF-IDF + AI for fast and accurate volunteer matching
- 📊 **Excel Import**: Bulk import volunteers from Excel files
- 🔄 **Google Sheets Sync**: Real-time sync with Google Forms/Sheets
- 💾 **MySQL Database**: Professional database with local or cloud support
- 📱 **Modern UI**: Beautiful, responsive web interface
- 🔍 **Smart Search**: Match volunteers with job requirements automatically
- 📈 **Real-time Stats**: View volunteer pool and shortlisted candidates

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

### 1. Setup MySQL Database

1. Install MySQL and open MySQL Workbench
2. Create database:
   ```sql
   CREATE DATABASE resumatch_db;
   ```

### 2. Configure Application

Edit `config.py`:
```python
MYSQL_USERNAME = "root"  # Your MySQL username
MYSQL_PASSWORD = "your_password"  # Your MySQL password
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Application

```bash
python app.py
```

Open browser: `http://localhost:5000`

### 5. (Optional) Import Sample Data

```bash
python create_sample_data.py
python excel_sync.py
```

## 💾 Database Support

**Two database options:**

### MySQL (Recommended)
- Better performance
- Professional database
- Easy to use with MySQL Workbench
- Supports concurrent users

### SQLite (Development)
- No setup required
- File-based database
- Good for testing

**Switch databases:** Change `DATABASE_TYPE` in `config.py`

See `DATABASE_SETUP.md` for detailed instructions.

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

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL (or SQLite for development)
- **AI**: Azure OpenAI (GPT-4) for keyword extraction
- **ML**: scikit-learn (TF-IDF, Cosine Similarity)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Processing**: Pandas, NumPy
- **Resume Parsing**: PyPDF2, python-docx
- **Cloud Sync**: Google Sheets API

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

