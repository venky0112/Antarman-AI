"""List available Gemini models"""

import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found")
    exit(1)

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("Available models:")
    for model in genai.list_models():
        print(f"  - {model.name}")
        print(f"    Display Name: {model.display_name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"    Supported methods: {model.supported_generation_methods}")
        print()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
