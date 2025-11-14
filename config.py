"""
Configuration file for ResuMatch VMS
Loads all configuration from .env file
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')

# Matching Configuration
MAX_VOLUNTEERS_TO_ANALYZE = int(os.getenv('MAX_VOLUNTEERS_TO_ANALYZE', 50))
TOP_MATCHES_TO_RETURN = int(os.getenv('TOP_MATCHES_TO_RETURN', 10))
MIN_MATCH_SCORE = int(os.getenv('MIN_MATCH_SCORE', 60))

# MySQL Database Configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'resumatch_db')
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_USE_SSL = os.getenv('MYSQL_USE_SSL', 'False').lower() == 'true'

# Application Configuration
PORT = int(os.getenv('PORT', 5000))
APP_HOST = os.getenv('APP_HOST', 'localhost')
APP_BASE_URL = os.getenv('APP_BASE_URL', f'http://{APP_HOST}:{PORT}')

# Validate required configuration
if not AZURE_OPENAI_API_KEY:
    raise ValueError("⚠️  AZURE_OPENAI_API_KEY is not set in .env file!")
if not AZURE_OPENAI_ENDPOINT:
    raise ValueError("⚠️  AZURE_OPENAI_ENDPOINT is not set in .env file!")
if not MYSQL_PASSWORD:
    raise ValueError("⚠️  MYSQL_PASSWORD is not set in .env file!")
