from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from resume_matcher import ResumeMatcher  # Back to TF-IDF matcher (fast!)
from keyword_extractor import KeywordExtractor  # AI for keyword extraction only
from resume_parser import ResumeParser
from database_mysql import MySQLDatabase
import json
import config

# Initialize MySQL database
db = MySQLDatabase(
    host=config.MYSQL_HOST,
    port=config.MYSQL_PORT,
    database=config.MYSQL_DATABASE,
    username=config.MYSQL_USERNAME,
    password=config.MYSQL_PASSWORD,
    use_ssl=config.MYSQL_USE_SSL
)
print(f"✅ Using MySQL Database: {config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}")

app = Flask(__name__)
CORS(app)

matcher = ResumeMatcher()  # Fast TF-IDF matching
keyword_extractor = KeywordExtractor()  # AI keyword extraction
parser = ResumeParser()

@app.route('/')
def index():
    """Serve the main frontend page"""
    return render_template('index.html')

@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    """Get all volunteers from database"""
    try:
        volunteers = db.get_all_volunteers()
        return jsonify({
            'success': True,
            'count': len(volunteers),
            'volunteers': volunteers
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/shortlist', methods=['POST'])
def shortlist_volunteers():
    """
    Shortlist volunteers using HYBRID approach:
    1. GPT-4 extracts keywords from job description (AI)
    2. TF-IDF matches volunteers using extracted keywords (Fast!)
    
    Expected JSON body:
    {
        "job_description": "Looking for Python developer with Django experience...",
        "max_results": 10,
        "min_score": 0.1
    }
    """
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        max_results = data.get('max_results', 10)
        min_score = data.get('min_score', 0.1)
        
        if not job_description:
            return jsonify({
                'success': False,
                'error': 'Job description is required'
            }), 400
        
        print("\n[API] Received job description")
        print("[AI] Step 1: Extracting keywords using GPT-4...")
        
        # STEP 1: Use GPT-4 to extract keywords (AI-powered understanding)
        keywords_data = keyword_extractor.extract_keywords(job_description)
        all_keywords = keywords_data.get('all_keywords', [])
        
        # Enhance job description with extracted keywords for better matching
        enhanced_description = job_description + " " + " ".join(all_keywords)
        
        print(f"[AI] Extracted {len(all_keywords)} keywords")
        print("[MATCHER] Step 2: Matching volunteers using TF-IDF (fast)...")
        
        # Get all volunteers from database
        volunteers = db.get_all_volunteers()
        
        if not volunteers:
            return jsonify({
                'success': False,
                'error': 'No volunteers found in database'
            }), 404
        
        # Clear previous shortlisted volunteers
        db.clear_shortlisted_volunteers()
        
        # STEP 2: Use TF-IDF matcher with enhanced description (fast matching)
        shortlisted = matcher.shortlist_volunteers(
            volunteers, 
            enhanced_description,
            min_score=min_score,
            max_results=max_results
        )
        
        # Insert shortlisted volunteers into database
        for item in shortlisted:
            volunteer = item['volunteer']
            match_score = item['match_score']
            matching_skills = json.dumps(item['matching_skills'])
            
            db.insert_shortlisted_volunteer(
                volunteer['id'],
                job_description,
                match_score,
                matching_skills
            )
        
        print(f"[SUCCESS] Found {len(shortlisted)} matching volunteers")
        
        return jsonify({
            'success': True,
            'count': len(shortlisted),
            'shortlisted': shortlisted,
            'extracted_keywords': all_keywords[:20],  # Return top 20 keywords for reference
            'ai_enhanced': True  # Flag to indicate AI keyword extraction was used
        })
        
    except Exception as e:
        print(f"\n[API ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/shortlisted', methods=['GET'])
def get_shortlisted_volunteers():
    """Get all shortlisted volunteers from database"""
    try:
        shortlisted = db.get_shortlisted_volunteers()
        
        # Parse matching_skills from JSON string
        for volunteer in shortlisted:
            try:
                volunteer['matching_skills'] = json.loads(volunteer['matching_skills'])
            except:
                volunteer['matching_skills'] = []
        
        return jsonify({
            'success': True,
            'count': len(shortlisted),
            'shortlisted': shortlisted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/shortlisted/clear', methods=['DELETE'])
def clear_shortlisted():
    """Clear all shortlisted volunteers"""
    try:
        db.clear_shortlisted_volunteers()
        return jsonify({
            'success': True,
            'message': 'Shortlisted volunteers cleared successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """
    Upload and parse resume file
    
    Accepts: PDF or DOCX files
    Extracts: Name, email, phone, skills, experience, education
    """
    try:
        if 'resume' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file extension
        if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
            return jsonify({
                'success': False,
                'error': 'Only PDF and DOCX files are supported'
            }), 400
        
        # Read file content
        file_content = file.read()
        
        # Parse resume
        volunteer_data = parser.parse_resume(file_content, file.filename)
        
        if not volunteer_data:
            return jsonify({
                'success': False,
                'error': 'Failed to parse resume. Please check file format.'
            }), 400
        
        # Validate required fields
        if not volunteer_data['email']:
            return jsonify({
                'success': False,
                'error': 'Could not extract email from resume. Please ensure email is clearly visible.'
            }), 400
        
        # Insert into database
        volunteer_id = db.insert_volunteer(volunteer_data)
        
        if volunteer_id:
            return jsonify({
                'success': True,
                'message': f'Successfully added {volunteer_data["name"]} to database',
                'volunteer': volunteer_data
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Email {volunteer_data["email"]} already exists'
            }), 409
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        volunteers = db.get_all_volunteers()
        shortlisted = db.get_shortlisted_volunteers()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_volunteers': len(volunteers),
                'shortlisted_count': len(shortlisted)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'ResuMatch-VMS',
        'timestamp': str(db.get_current_timestamp()) if hasattr(db, 'get_current_timestamp') else None
    }), 200

@app.route('/health/detailed', methods=['GET'])
@app.route('/api/health/detailed', methods=['GET'])
def detailed_health_check():
    """Detailed health check with all component status"""
    health_status = {
        'status': 'healthy',
        'service': 'ResuMatch-VMS',
        'components': {}
    }
    
    # Check Database
    try:
        db.get_all_volunteers()
        health_status['components']['database'] = {
            'status': 'healthy',
            'type': 'MySQL',
            'host': config.MYSQL_HOST
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['components']['database'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
    
    # Check AI Services (Azure OpenAI)
    try:
        if config.AZURE_OPENAI_API_KEY and config.AZURE_OPENAI_ENDPOINT:
            health_status['components']['ai_service'] = {
                'status': 'configured',
                'provider': 'Azure OpenAI',
                'deployment': config.AZURE_OPENAI_DEPLOYMENT
            }
        else:
            health_status['components']['ai_service'] = {
                'status': 'not_configured',
                'warning': 'Azure OpenAI credentials not set'
            }
    except Exception as e:
        health_status['components']['ai_service'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Check Resume Matcher
    try:
        if matcher:
            health_status['components']['resume_matcher'] = {
                'status': 'ready',
                'type': 'TF-IDF'
            }
        else:
            health_status['components']['resume_matcher'] = {
                'status': 'not_initialized'
            }
    except Exception as e:
        health_status['components']['resume_matcher'] = {
            'status': 'error',
            'error': str(e)
        }
    
    # Check Resume Parser
    try:
        if parser:
            health_status['components']['resume_parser'] = {
                'status': 'ready'
            }
        else:
            health_status['components']['resume_parser'] = {
                'status': 'not_initialized'
            }
    except Exception as e:
        health_status['components']['resume_parser'] = {
            'status': 'error',
            'error': str(e)
        }
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎯 ResuMatch VMS - Starting Server...")
    print("="*60)
    print("\n✅ Database connected and ready!")
    print(f"✅ Server starting at http://localhost:{config.PORT}")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=config.PORT)

