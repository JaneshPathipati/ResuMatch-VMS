import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_name='volunteer_management.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create volunteers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                skills TEXT,
                experience TEXT,
                education TEXT,
                availability TEXT,
                languages TEXT,
                certifications TEXT,
                interests TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create shortlisted_volunteers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shortlisted_volunteers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                volunteer_id INTEGER NOT NULL,
                job_description TEXT NOT NULL,
                match_score REAL,
                matching_skills TEXT,
                shortlisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (volunteer_id) REFERENCES volunteers (id)
            )
        ''')
        
        # Create job_postings table for reference
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_postings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                required_skills TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully!")
    
    def insert_volunteer(self, volunteer_data):
        """Insert a new volunteer into the database with expanded schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic INSERT statement based on provided fields
            fields = []
            values = []
            
            # Core fields (always required)
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
                # Expanded fields
                'timestamp': 'timestamp',
                'prefix': 'prefix',
                'alternate_phone': 'alternate_phone',
                'date_of_birth': 'date_of_birth',
                'anniversary_date': 'anniversary_date',
                'gender': 'gender',
                'country': 'country',
                'state': 'state',
                'city': 'city',
                'address': 'address',
                'pin_code': 'pin_code',
                'zip_code': 'zip_code',
                'education_field': 'education_field',
                'job_sector': 'job_sector',
                'profession': 'profession',
                'job_position': 'job_position',
                'years_experience': 'years_experience',
                'linkedin_url': 'linkedin_url',
                'facebook_url': 'facebook_url',
                'instagram_url': 'instagram_url',
                'previous_experience': 'previous_experience',
                'primary_skills': 'primary_skills',
                'secondary_skills': 'secondary_skills',
                'volunteering_mode': 'volunteering_mode',
                'availability_days': 'availability_days',
                'time_availability': 'time_availability',
                'commitment_duration': 'commitment_duration',
                'join_date': 'join_date',
                'hear_about_source': 'hear_about_source',
                'passed_examination': 'passed_examination',
                'departments_served': 'departments_served',
                'journey_description': 'journey_description',
            }
            
            for key, db_field in field_mapping.items():
                if key in volunteer_data:
                    fields.append(db_field)
                    values.append(volunteer_data[key])
            
            # Construct the SQL query
            placeholders = ', '.join(['?' for _ in fields])
            fields_str = ', '.join(fields)
            
            sql = f"INSERT INTO volunteers ({fields_str}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            # print(f"Error inserting volunteer: {e}")
            return None
        finally:
            conn.close()
    
    def get_all_volunteers(self):
        """Retrieve all volunteers from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM volunteers')
        columns = [description[0] for description in cursor.description]
        volunteers = []
        
        for row in cursor.fetchall():
            volunteers.append(dict(zip(columns, row)))
        
        conn.close()
        return volunteers
    
    def insert_shortlisted_volunteer(self, volunteer_id, job_description, match_score, matching_skills):
        """Insert a shortlisted volunteer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO shortlisted_volunteers 
            (volunteer_id, job_description, match_score, matching_skills)
            VALUES (?, ?, ?, ?)
        ''', (volunteer_id, job_description, match_score, matching_skills))
        
        conn.commit()
        conn.close()
    
    def get_shortlisted_volunteers(self):
        """Retrieve all shortlisted volunteers with their details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
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
        
        columns = [description[0] for description in cursor.description]
        shortlisted = []
        
        for row in cursor.fetchall():
            shortlisted.append(dict(zip(columns, row)))
        
        conn.close()
        return shortlisted
    
    def clear_shortlisted_volunteers(self):
        """Clear all shortlisted volunteers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shortlisted_volunteers')
        conn.commit()
        conn.close()
    
    def clear_all_data(self):
        """Clear all data from all tables (for testing)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM shortlisted_volunteers')
        cursor.execute('DELETE FROM volunteers')
        cursor.execute('DELETE FROM job_postings')
        conn.commit()
        conn.close()

