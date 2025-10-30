"""
Azure OpenAI Configuration Diagnostics
Helps identify issues with Azure OpenAI setup
"""

try:
    from config import (
        AZURE_OPENAI_API_KEY,
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_DEPLOYMENT,
        AZURE_OPENAI_API_VERSION
    )
except ImportError:
    print("\n❌ ERROR: config.py not found!")
    print("Please copy config.example.py to config.py and add your credentials.")
    exit(1)

print("\n" + "="*80)
print(" AZURE OPENAI CONFIGURATION DIAGNOSTICS")
print("="*80)

print("\n📋 Current Configuration:")
print("-" * 80)
print(f"API Key: {AZURE_OPENAI_API_KEY[:20]}...{AZURE_OPENAI_API_KEY[-10:]} (masked)")
print(f"Endpoint: {AZURE_OPENAI_ENDPOINT}")
print(f"Deployment Name: {AZURE_OPENAI_DEPLOYMENT}")
print(f"API Version: {AZURE_OPENAI_API_VERSION}")

print("\n" + "="*80)
print(" ⚠️ ISSUES DETECTED")
print("="*80)

print("\n1. ❌ DEPLOYMENT NAME: 'gpt-4.1'")
print("   Problem: This deployment name doesn't exist")
print("   Solution: Use the EXACT deployment name from Azure Portal")
print()
print("   Common deployment names:")
print("   ✅ gpt-4")
print("   ✅ gpt-4-turbo")
print("   ✅ gpt-35-turbo")
print("   ✅ gpt-4o")
print("   ✅ text-embedding-ada-002")

print("\n2. ❌ API VERSION: '2025-04-14'")
print("   Problem: This is a future date (doesn't exist yet)")
print("   Solution: Use a valid Azure OpenAI API version")
print()
print("   Valid API versions:")
print("   ✅ 2024-02-15-preview")
print("   ✅ 2024-05-01-preview")
print("   ✅ 2024-06-01")
print("   ✅ 2024-08-01-preview")
print("   ✅ 2024-10-01-preview")

print("\n" + "="*80)
print(" 🔍 HOW TO FIND CORRECT VALUES")
print("="*80)

print("\n1. Go to Azure Portal: https://portal.azure.com")
print("2. Navigate to: Azure OpenAI Resource → Deployments")
print("3. Find your GPT-4 deployment")
print("4. Note the EXACT 'Deployment name' (e.g., 'gpt-4' or 'my-gpt4-deployment')")
print("5. Use a valid API version from the list above")

print("\n" + "="*80)
print(" 📝 RECOMMENDED CONFIGURATION")
print("="*80)

print("\n# Most common setup for GPT-4:")
print("AZURE_OPENAI_API_KEY = 'your-api-key-here'")
print("AZURE_OPENAI_ENDPOINT = 'https://your-resource.cognitiveservices.azure.com/'")
print("AZURE_OPENAI_DEPLOYMENT = 'gpt-4'  # ⬅️ Change this to your actual deployment name")
print("AZURE_OPENAI_API_VERSION = '2024-08-01-preview'  # ⬅️ Use a valid version")

print("\n" + "="*80)
print(" ✅ NEXT STEPS")
print("="*80)

print("\n1. Check your Azure Portal for the correct deployment name")
print("2. Update config.py with:")
print("   - Correct deployment name (from Azure Portal)")
print("   - Valid API version (e.g., '2024-08-01-preview')")
print("3. Run: python test_ai_connection.py")
print("4. If successful, run: python ai_matcher.py")

print("\n" + "="*80 + "\n")

print("❓ Need help finding your deployment name?")
print("   Look in: Azure Portal → Your OpenAI Resource → Model deployments")
print("   The 'Name' column shows your deployment name (NOT the model name)")
print()

