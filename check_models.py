import google.generativeai as genai

# Replace with your API key
API_KEY = "AIzaSyACCwiHbstl1oTKLY7v84eU0tbafyFBtIQ"

genai.configure(api_key=API_KEY)

print("Available Gemini models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"  - {model.name}")