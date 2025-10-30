"""
Configuration file for Azure OpenAI
INSTRUCTIONS: 
1. Copy this file to config.py
2. Fill in your actual Azure OpenAI credentials
3. Never commit config.py to Git (it's in .gitignore)
"""

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.cognitiveservices.azure.com/"
AZURE_OPENAI_DEPLOYMENT = "gpt-4.1"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"

# Matching Configuration
MAX_VOLUNTEERS_TO_ANALYZE = 50  # Analyze top 50 candidates in detail
TOP_MATCHES_TO_RETURN = 10  # Return top 10 best matches
MIN_MATCH_SCORE = 60  # Minimum score to be considered a match (0-100)

