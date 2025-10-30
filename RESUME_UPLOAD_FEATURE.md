# 📄 Resume Upload Feature

## Overview
HR can now upload single or multiple volunteer resumes (PDF or DOCX) and the system will automatically extract relevant data and add volunteers to the database.

## ✨ Features

### Automatic Data Extraction
The AI-powered resume parser extracts:
- ✅ **Name** - From the header of the resume
- ✅ **Email** - Email address detection
- ✅ **Phone** - Multiple phone formats supported
- ✅ **Skills** - Technical and soft skills identification
- ✅ **Experience** - Work experience summary
- ✅ **Education** - Degrees and qualifications

### Supported File Formats
- **PDF** (.pdf)
- **Word Documents** (.docx, .doc)

### File Validation
- Maximum file size: 10MB
- Only PDF and DOCX formats accepted
- Duplicate email detection (won't add same volunteer twice)

---

## 🚀 How to Use

### Step 1: Access the Upload Section
Open the web interface at http://localhost:5000

You'll see a new "📄 Upload Resume" section at the top.

### Step 2: Select Resume File(s)
1. Click "Choose File" button
2. Select one or multiple PDF/DOCX resumes from your computer
   - Hold Ctrl (Windows) or Cmd (Mac) to select multiple files
3. Click "📤 Upload Resumes"

### Step 3: View Results
The system will:
1. Parse the resume (takes 2-5 seconds)
2. Extract volunteer data automatically
3. Insert into database
4. Show extracted information on screen

### Example Success Message:
```
✓ Resume parsed successfully! Added John Doe to database.

Extracted Data:
• Name: John Doe
• Email: john.doe@email.com  
• Phone: +1-234-567-8900
• Skills: Python, Django, React, JavaScript, SQL, Testing...
```

---

## 🎯 Resume Format Tips

For best results, resumes should include:

### Required Fields
- **Email address** - Must be clearly visible (required)
- **Name** - Usually at the top of resume

### Recommended Fields
- **Phone number** - In standard formats
- **Skills section** - Clearly labeled "Skills" or "Technical Skills"
- **Experience section** - Work history
- **Education section** - Degrees and qualifications

### Supported Phone Formats
- +1-234-567-8900
- (234) 567-8900
- 234-567-8900
- 2345678900
- +91 1234567890

### Skills Detection
The parser automatically detects 50+ common skills including:
- Programming: Python, Java, JavaScript, PHP, C++, etc.
- Frameworks: React, Angular, Django, Flask, Spring, etc.
- Databases: MySQL, PostgreSQL, MongoDB, SQL, etc.
- DevOps: Docker, Kubernetes, AWS, Azure, Jenkins, etc.
- Design: Graphic Design, UI/UX, Figma, Photoshop, etc.
- Other: Testing, QA, Agile, Digital Marketing, etc.

---

## 🔧 Technical Details

### Backend API Endpoint
```
POST /api/upload-resume
Content-Type: multipart/form-data
```

**Request:**
```
FormData:
  resume: <file>
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Resume parsed successfully! Added John Doe to database.",
  "volunteer": {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1-234-567-8900",
    "skills": "Python, Django, React...",
    "experience": "5 years of software development...",
    "education": "Bachelor of Computer Science"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Could not extract email from resume..."
}
```

### Resume Parser Module
File: `resume_parser.py`

**Key Methods:**
- `parse_resume(file_content, filename)` - Main parsing function
- `extract_email(text)` - Extract email using regex
- `extract_phone(text)` - Extract phone numbers
- `extract_skills(text)` - Identify technical skills
- `extract_experience(text)` - Parse work experience
- `extract_education(text)` - Extract education details

---

## ⚠️ Error Handling

### Common Errors

**"No file uploaded"**
- Solution: Select a file before clicking upload

**"Only PDF and DOCX files are supported"**
- Solution: Convert resume to PDF or DOCX format

**"Could not extract email from resume"**
- Solution: Ensure email is clearly visible in the resume

**"Volunteer with email [email] already exists"**
- Solution: This volunteer is already in the database (duplicate)

**"File size too large. Maximum size is 10MB"**
- Solution: Compress or optimize the resume file

---

## 📊 Database Storage

Parsed resume data is stored in the `volunteers` table:

```sql
INSERT INTO volunteers (
  name, email, phone, skills, experience, 
  education, availability, languages, 
  certifications, interests
) VALUES (...)
```

Fields not found in resume are set to "Not specified".

---

## 🎨 Frontend Components

### Upload Button
- Color: Green gradient
- Icon: 📤
- States: Normal, Loading, Disabled

### File Input
- Dashed border for drag-and-drop feel
- Accepts: .pdf, .docx, .doc
- Max size: 10MB

### Status Messages
- Success: Green background
- Error: Red background
- Shows extracted data after successful parse

---

## 🧪 Testing

### Test the Feature:

1. **Valid Resume Test:**
   - Upload a well-formatted PDF/DOCX resume
   - Should extract all fields successfully

2. **Duplicate Email Test:**
   - Upload same resume twice
   - Should show "already exists" error

3. **Invalid File Test:**
   - Try uploading .txt or .jpg file
   - Should show format error

4. **Large File Test:**
   - Try uploading >10MB file
   - Should show size error

5. **Resume Without Email:**
   - Upload resume without email
   - Should show email extraction error

---

## 💡 Future Enhancements

Potential improvements:
- [x] ✅ Batch upload (multiple resumes at once) - IMPLEMENTED
- [ ] OCR for scanned/image PDFs
- [ ] More detailed experience parsing (dates, companies)
- [ ] Certification extraction
- [ ] Language proficiency levels
- [ ] Download extracted data as CSV
- [ ] Resume preview before upload
- [ ] Support for more file formats (TXT, RTF)

---

## 📝 Example Use Cases

### Use Case 1: Volunteer Registration Event
- Collect resumes from volunteers at registration desk
- Upload them through web interface
- Automatically populate database
- Use AI matching to assign to appropriate projects

### Use Case 2: Email Submissions
- Volunteers email their resumes
- Save resume files to computer
- Upload through web interface
- Instant addition to volunteer pool

### Use Case 3: Bulk Import
- Have folder of 100+ resumes
- Select and upload multiple resumes at once
- System processes each resume automatically
- Build comprehensive volunteer database quickly
- Match volunteers to multiple projects

---

## ✅ Success Criteria

A resume is considered successfully parsed if:
1. ✅ Email is extracted (required)
2. ✅ Name is extracted
3. ✅ At least one skill is identified
4. ✅ Data is inserted into database
5. ✅ No duplicate email conflicts

---

**The resume upload feature is now fully functional!** 🎉

Upload resumes at: http://localhost:5000

