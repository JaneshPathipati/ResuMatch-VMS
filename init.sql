-- Initialize ResuMatch VMS Database Schema

USE resumatch_db;

-- Create volunteers table
CREATE TABLE IF NOT EXISTS volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    skills TEXT,
    experience TEXT,
    education TEXT,
    availability VARCHAR(255),
    languages VARCHAR(255),
    certifications TEXT,
    interests TEXT,
    resume_text LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create shortlisted_volunteers table
CREATE TABLE IF NOT EXISTS shortlisted_volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    volunteer_id INT NOT NULL,
    job_description TEXT,
    match_score FLOAT,
    matching_skills TEXT,
    job_keywords TEXT,
    shortlisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id) ON DELETE CASCADE,
    INDEX idx_volunteer_id (volunteer_id),
    INDEX idx_match_score (match_score),
    INDEX idx_shortlisted_at (shortlisted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data (optional - for testing)
-- You can comment this out for production
INSERT IGNORE INTO volunteers (name, email, phone, skills, experience, education, availability, languages, certifications, interests)
VALUES 
    ('John Doe', 'john.doe@example.com', '+1234567890', 'Python, Flask, MySQL, Docker', '3 years in web development', 'B.Tech Computer Science', 'Full-time', 'English, Spanish', 'AWS Certified', 'Open source, AI/ML'),
    ('Jane Smith', 'jane.smith@example.com', '+1234567891', 'JavaScript, React, Node.js', '2 years frontend development', 'B.Sc Software Engineering', 'Part-time', 'English', 'React Certification', 'Web design, UX'),
    ('Bob Wilson', 'bob.wilson@example.com', '+1234567892', 'Java, Spring Boot, Microservices', '5 years backend development', 'M.Tech Computer Science', 'Full-time', 'English, French', 'Java Oracle Certified', 'System design, Cloud');

