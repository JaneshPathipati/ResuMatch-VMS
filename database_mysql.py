import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json

class MySQLDatabase:
    def __init__(self, host=None, port=3306, database=None, username=None, password=None, use_ssl=True):
        """
        Initialize MySQL Database connection (MySQL HeatWave compatible)
        
        Args:
            host: MySQL host (IP or hostname)
            port: MySQL port (default: 3306)
            database: Database name
            username: MySQL username
            password: MySQL password
            use_ssl: Use SSL/TLS connection (recommended for cloud)
        """
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.init_database()
    
    def get_connection(self):
        """Get MySQL database connection"""
        try:
            config = {
                'host': self.host,
                'port': self.port,
                'database': self.database,
                'user': self.username,
                'password': self.password,
                'autocommit': False,
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci'
            }
            
            # Add SSL configuration for secure connection
            if self.use_ssl:
                config['ssl_disabled'] = False
            
            return mysql.connector.connect(**config)
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create volunteers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS volunteers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    email VARCHAR(200) UNIQUE NOT NULL,
                    phone VARCHAR(50),
                    skills TEXT,
                    experience TEXT,
                    education VARCHAR(500),
                    availability VARCHAR(200),
                    languages VARCHAR(200),
                    certifications TEXT,
                    interests TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_email (email),
                    INDEX idx_name (name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("✅ Volunteers table ready")
            
            # Create shortlisted_volunteers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shortlisted_volunteers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    volunteer_id INT NOT NULL,
                    job_description TEXT NOT NULL,
                    match_score DECIMAL(5,2),
                    matching_skills TEXT,
                    shortlisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
                    INDEX idx_volunteer_id (volunteer_id),
                    INDEX idx_match_score (match_score)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("✅ Shortlisted_volunteers table ready")
            
            # Create job_postings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_postings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(300) NOT NULL,
                    description TEXT NOT NULL,
                    required_skills TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("✅ Job_postings table ready")
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ MySQL Database initialized successfully!")
            
        except Error as e:
            print(f"Error initializing database: {e}")
            raise
    
    def insert_volunteer(self, volunteer_data):
        """Insert a new volunteer into the database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Core fields mapping
            fields = []
            values = []
            placeholders = []
            
            field_mapping = {
                'name': 'name',
                'email': 'email',
                'phone': 'phone',
                'skills': 'skills',
                'experience': 'experience',
                'education': 'education',
                'availability': 'availability',
                'languages': 'languages',
                'certifications': 'certifications',
                'interests': 'interests',
            }
            
            for key, db_field in field_mapping.items():
                if key in volunteer_data:
                    fields.append(db_field)
                    values.append(volunteer_data[key])
                    placeholders.append('%s')
            
            # Construct the SQL query
            fields_str = ', '.join(fields)
            placeholders_str = ', '.join(placeholders)
            
            sql = f"INSERT INTO volunteers ({fields_str}) VALUES ({placeholders_str})"
            cursor.execute(sql, values)
            
            volunteer_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            conn.close()
            return volunteer_id
            
        except mysql.connector.IntegrityError:
            # Duplicate email
            return None
        except Error as e:
            print(f"Error inserting volunteer: {e}")
            return None
    
    def get_all_volunteers(self):
        """Retrieve all volunteers from the database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM volunteers ORDER BY id')
            volunteers = cursor.fetchall()
            
            # Convert datetime objects to strings
            for volunteer in volunteers:
                if 'created_at' in volunteer and volunteer['created_at']:
                    volunteer['created_at'] = volunteer['created_at'].isoformat()
            
            cursor.close()
            conn.close()
            return volunteers
            
        except Error as e:
            print(f"Error retrieving volunteers: {e}")
            return []
    
    def insert_shortlisted_volunteer(self, volunteer_id, job_description, match_score, matching_skills):
        """Insert a shortlisted volunteer"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO shortlisted_volunteers 
                (volunteer_id, job_description, match_score, matching_skills)
                VALUES (%s, %s, %s, %s)
            ''', (volunteer_id, job_description, match_score, matching_skills))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Error as e:
            print(f"Error inserting shortlisted volunteer: {e}")
    
    def get_shortlisted_volunteers(self):
        """Retrieve all shortlisted volunteers with their details"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('''
                SELECT 
                    s.id,
                    v.name,
                    v.email,
                    v.phone,
                    v.skills,
                    v.experience,
                    v.education,
                    s.job_description,
                    s.match_score,
                    s.matching_skills,
                    s.shortlisted_at
                FROM shortlisted_volunteers s
                JOIN volunteers v ON s.volunteer_id = v.id
                ORDER BY s.match_score DESC, s.shortlisted_at DESC
            ''')
            
            shortlisted = cursor.fetchall()
            
            # Convert datetime objects to strings
            for item in shortlisted:
                if 'shortlisted_at' in item and item['shortlisted_at']:
                    item['shortlisted_at'] = item['shortlisted_at'].isoformat()
            
            cursor.close()
            conn.close()
            return shortlisted
            
        except Error as e:
            print(f"Error retrieving shortlisted volunteers: {e}")
            return []
    
    def clear_shortlisted_volunteers(self):
        """Clear all shortlisted volunteers"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM shortlisted_volunteers')
            conn.commit()
            cursor.close()
            conn.close()
            
        except Error as e:
            print(f"Error clearing shortlisted volunteers: {e}")
    
    def clear_all_data(self):
        """Clear all data from all tables (for testing)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM shortlisted_volunteers')
            cursor.execute('DELETE FROM volunteers')
            cursor.execute('DELETE FROM job_postings')
            conn.commit()
            cursor.close()
            conn.close()
            
        except Error as e:
            print(f"Error clearing all data: {e}")
    
    def test_connection(self):
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return True
        except Error as e:
            print(f"Connection test failed: {e}")
            return False

