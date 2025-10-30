"""
Quick test to verify Azure OpenAI connection
"""

from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
)

print("\n" + "="*80)
print(" TESTING AZURE OPENAI CONNECTION")
print("="*80)

print(f"\nEndpoint: {AZURE_OPENAI_ENDPOINT}")
print(f"Deployment: {AZURE_OPENAI_DEPLOYMENT}")
print(f"API Version: {AZURE_OPENAI_API_VERSION}")
print(f"API Key: {AZURE_OPENAI_API_KEY[:20]}..." if len(AZURE_OPENAI_API_KEY) > 20 else "***")

print("\n" + "-"*80)
print("Testing connection...")
print("-"*80)

try:
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )
    
    print("\n[1/2] Client created successfully")
    
    # Test a simple completion
    print("[2/2] Sending test request to GPT-4...")
    
    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Connection successful!' if you can read this."}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    result = response.choices[0].message.content
    
    print("\n" + "="*80)
    print(" SUCCESS!")
    print("="*80)
    print(f"\nGPT-4 Response: {result}")
    print(f"\nConnection to Azure OpenAI is working perfectly!")
    print("="*80 + "\n")
    
except Exception as e:
    print("\n" + "="*80)
    print(" ERROR!")
    print("="*80)
    print(f"\nFailed to connect to Azure OpenAI: {e}")
    print("\nPossible issues:")
    print("  1. Check if the API key is correct")
    print("  2. Check if the endpoint URL is correct")
    print("  3. Check if the deployment name exists")
    print("  4. Check if the API version is valid")
    print("="*80 + "\n")
    
    import traceback
    traceback.print_exc()

