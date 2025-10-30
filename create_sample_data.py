import pandas as pd

# Sample volunteer data for demonstration
volunteers_data = [
    {
        'Name': 'John Smith',
        'Email': 'john.smith@email.com',
        'Phone': '+1-555-0101',
        'Skills': 'Python, Django, Flask, REST API, SQL, JavaScript, React',
        'Experience': '3 years web development, 2 years volunteer coordination',
        'Education': 'Bachelor of Computer Science',
        'Availability': 'Weekends and evenings',
        'Languages': 'English, Spanish',
        'Certifications': 'AWS Certified Developer',
        'Interests': 'Web development, community outreach, education'
    },
    {
        'Name': 'Sarah Johnson',
        'Email': 'sarah.j@email.com',
        'Phone': '+1-555-0102',
        'Skills': 'Java, Spring Boot, MySQL, Docker, Kubernetes, Agile',
        'Experience': '5 years software engineering, team leadership',
        'Education': 'Master of Software Engineering',
        'Availability': 'Flexible schedule',
        'Languages': 'English, French, Mandarin',
        'Certifications': 'Scrum Master, PMP',
        'Interests': 'Backend development, mentoring, open source'
    },
    {
        'Name': 'Michael Chen',
        'Email': 'mchen@email.com',
        'Phone': '+1-555-0103',
        'Skills': 'React, Angular, TypeScript, CSS, UI/UX Design, Figma',
        'Experience': '4 years frontend development, UI design',
        'Education': 'Bachelor of Design and Technology',
        'Availability': 'Weekdays after 6 PM',
        'Languages': 'English, Cantonese',
        'Certifications': 'Google UX Design Certificate',
        'Interests': 'Frontend development, user experience, accessibility'
    },
    {
        'Name': 'Emily Rodriguez',
        'Email': 'emily.r@email.com',
        'Phone': '+1-555-0104',
        'Skills': 'Data Analysis, Python, R, Machine Learning, TensorFlow, SQL',
        'Experience': '3 years data science, statistical analysis',
        'Education': 'Master of Data Science',
        'Availability': 'Weekends',
        'Languages': 'English, Spanish, Portuguese',
        'Certifications': 'IBM Data Science Professional Certificate',
        'Interests': 'Machine learning, data visualization, education'
    },
    {
        'Name': 'David Wilson',
        'Email': 'dwilson@email.com',
        'Phone': '+1-555-0105',
        'Skills': 'Node.js, Express, MongoDB, GraphQL, AWS, DevOps',
        'Experience': '6 years full-stack development, cloud architecture',
        'Education': 'Bachelor of Computer Engineering',
        'Availability': 'Evenings and weekends',
        'Languages': 'English',
        'Certifications': 'AWS Solutions Architect, MongoDB Certified Developer',
        'Interests': 'Cloud computing, scalable systems, tech education'
    },
    {
        'Name': 'Lisa Thompson',
        'Email': 'lisa.t@email.com',
        'Phone': '+1-555-0106',
        'Skills': 'Project Management, Agile, Communication, Leadership, Stakeholder Management',
        'Experience': '8 years project management, nonprofit sector',
        'Education': 'MBA, Bachelor of Business Administration',
        'Availability': 'Flexible, prefer daytime',
        'Languages': 'English, German',
        'Certifications': 'PMP, Agile Certified Practitioner',
        'Interests': 'Project coordination, team building, community development'
    },
    {
        'Name': 'James Martinez',
        'Email': 'jmartinez@email.com',
        'Phone': '+1-555-0107',
        'Skills': 'C++, C#, Unity, Game Development, Graphics Programming',
        'Experience': '4 years game development, 3D graphics',
        'Education': 'Bachelor of Computer Science',
        'Availability': 'Weekends',
        'Languages': 'English, Spanish',
        'Certifications': 'Unity Certified Developer',
        'Interests': 'Game development, graphics, educational games'
    },
    {
        'Name': 'Rachel Kim',
        'Email': 'rachel.kim@email.com',
        'Phone': '+1-555-0108',
        'Skills': 'Cybersecurity, Network Security, Penetration Testing, Python, Linux',
        'Experience': '5 years information security, security auditing',
        'Education': 'Master of Cybersecurity',
        'Availability': 'Evenings',
        'Languages': 'English, Korean',
        'Certifications': 'CISSP, CEH, Security+',
        'Interests': 'Security awareness, privacy advocacy, tech policy'
    },
    {
        'Name': 'Chris Anderson',
        'Email': 'canderson@email.com',
        'Phone': '+1-555-0109',
        'Skills': 'Mobile Development, Flutter, React Native, iOS, Android, Firebase',
        'Experience': '4 years mobile app development',
        'Education': 'Bachelor of Software Engineering',
        'Availability': 'Weekends and holidays',
        'Languages': 'English',
        'Certifications': 'Google Associate Android Developer',
        'Interests': 'Mobile apps, user engagement, social impact apps'
    },
    {
        'Name': 'Amanda White',
        'Email': 'awhite@email.com',
        'Phone': '+1-555-0110',
        'Skills': 'Content Writing, Technical Writing, Documentation, Markdown, Git',
        'Experience': '5 years technical writing, developer documentation',
        'Education': 'Bachelor of English, Technical Communication Certificate',
        'Availability': 'Weekdays and some weekends',
        'Languages': 'English, Italian',
        'Certifications': 'Technical Writing Certification',
        'Interests': 'Documentation, knowledge sharing, open source'
    },
    {
        'Name': 'Kevin Brown',
        'Email': 'kbrown@email.com',
        'Phone': '+1-555-0111',
        'Skills': 'DevOps, CI/CD, Jenkins, Docker, Kubernetes, Terraform, Azure',
        'Experience': '6 years DevOps engineering, infrastructure automation',
        'Education': 'Bachelor of Information Technology',
        'Availability': 'Flexible schedule',
        'Languages': 'English',
        'Certifications': 'Azure DevOps Engineer Expert, CKA',
        'Interests': 'Automation, infrastructure as code, cloud platforms'
    },
    {
        'Name': 'Jennifer Lee',
        'Email': 'jlee@email.com',
        'Phone': '+1-555-0112',
        'Skills': 'Digital Marketing, SEO, Social Media, Content Strategy, Analytics',
        'Experience': '4 years digital marketing, nonprofit campaigns',
        'Education': 'Bachelor of Marketing',
        'Availability': 'Weekdays after work',
        'Languages': 'English, Korean, Japanese',
        'Certifications': 'Google Analytics, HubSpot Content Marketing',
        'Interests': 'Community engagement, social impact, storytelling'
    },
    {
        'Name': 'Robert Taylor',
        'Email': 'rtaylor@email.com',
        'Phone': '+1-555-0113',
        'Skills': 'Database Administration, PostgreSQL, MySQL, Oracle, Performance Tuning',
        'Experience': '7 years database administration, data architecture',
        'Education': 'Bachelor of Computer Science',
        'Availability': 'Evenings',
        'Languages': 'English',
        'Certifications': 'Oracle Certified Professional, PostgreSQL Certified',
        'Interests': 'Data management, optimization, teaching'
    },
    {
        'Name': 'Nicole Garcia',
        'Email': 'ngarcia@email.com',
        'Phone': '+1-555-0114',
        'Skills': 'Graphic Design, Adobe Creative Suite, Branding, UI Design, Illustration',
        'Experience': '5 years graphic design, volunteer for nonprofits',
        'Education': 'Bachelor of Fine Arts, Graphic Design',
        'Availability': 'Weekends',
        'Languages': 'English, Spanish',
        'Certifications': 'Adobe Certified Expert',
        'Interests': 'Visual design, nonprofit branding, community arts'
    },
    {
        'Name': 'Thomas Davis',
        'Email': 'tdavis@email.com',
        'Phone': '+1-555-0115',
        'Skills': 'Quality Assurance, Test Automation, Selenium, Jest, Cypress, API Testing',
        'Experience': '4 years QA engineering, test automation',
        'Education': 'Bachelor of Computer Science',
        'Availability': 'Flexible, prefer remote',
        'Languages': 'English',
        'Certifications': 'ISTQB Certified Tester',
        'Interests': 'Software quality, automation, continuous improvement'
    }
]

# Create DataFrame
df = pd.DataFrame(volunteers_data)

# Save to Excel
excel_filename = 'volunteers_data.xlsx'
df.to_excel(excel_filename, index=False, engine='openpyxl')

print(f"[SUCCESS] Sample volunteer data created successfully!")
print(f"  File: {excel_filename}")
print(f"  Records: {len(volunteers_data)} volunteers")
print("\nYou can now run 'python excel_sync.py' to sync this data to the database.")

