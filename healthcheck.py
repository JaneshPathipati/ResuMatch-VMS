#!/usr/bin/env python3
"""
Health Check Script for ResuMatch-VMS
Checks the health of all system components
"""

import sys
import os
import requests
import mysql.connector
from mysql.connector import Error
import config

def check_flask_app():
    """Check if Flask application is responding"""
    try:
        port = config.PORT
        response = requests.get(f'http://localhost:{port}/health', timeout=5)
        if response.status_code == 200:
            print("✅ Flask App: Healthy")
            return True
        else:
            print(f"❌ Flask App: Unhealthy (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Flask App: Not responding ({e})")
        return False

def check_database():
    """Check if MySQL database is accessible"""
    try:
        conn = mysql.connector.connect(
            host=config.MYSQL_HOST,
            port=config.MYSQL_PORT,
            database=config.MYSQL_DATABASE,
            user=config.MYSQL_USERNAME,
            password=config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        print("✅ MySQL Database: Healthy")
        return True
    except Error as e:
        print(f"❌ MySQL Database: Unhealthy ({e})")
        return False

def check_ai_service():
    """Check if Azure OpenAI credentials are configured"""
    try:
        if config.AZURE_OPENAI_API_KEY and config.AZURE_OPENAI_ENDPOINT:
            print(f"✅ Azure OpenAI: Configured (Deployment: {config.AZURE_OPENAI_DEPLOYMENT})")
            return True
        else:
            print("⚠️  Azure OpenAI: Not configured")
            return False
    except Exception as e:
        print(f"❌ Azure OpenAI: Configuration error ({e})")
        return False

def check_detailed_health():
    """Check detailed health endpoint"""
    try:
        port = config.PORT
        response = requests.get(f'http://localhost:{port}/health/detailed', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("\n📊 Detailed Health Status:")
            print(f"   Overall Status: {data.get('status', 'unknown').upper()}")
            
            components = data.get('components', {})
            for component, details in components.items():
                status = details.get('status', 'unknown')
                status_symbol = "✅" if status in ['healthy', 'ready', 'configured'] else "⚠️" if status == 'not_configured' else "❌"
                print(f"   {status_symbol} {component}: {status}")
                
                if 'error' in details:
                    print(f"      Error: {details['error']}")
            return True
        else:
            print(f"❌ Detailed Health Check: Failed (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Detailed Health Check: Not available ({e})")
        return False

def main():
    """Main health check function"""
    print("="*60)
    print("🏥 ResuMatch-VMS Health Check")
    print("="*60)
    print()
    
    checks = {
        'Flask App': check_flask_app(),
        'Database': check_database(),
        'AI Service': check_ai_service()
    }
    
    print()
    check_detailed_health()
    
    print()
    print("="*60)
    
    all_healthy = all(checks.values())
    
    if all_healthy:
        print("✅ All critical components are healthy!")
        print("="*60)
        return 0
    else:
        print("❌ Some components are unhealthy. Please check the logs.")
        print("="*60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
