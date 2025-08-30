import os
import sys
from dotenv import load_dotenv
from google import genai

if sys.argv[1:] == []: # quit if nothing provided to pass into gemini
    sys.exit(1)

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

gemini_response = client.models.generate_content(model='gemini-2.0-flash-001', contents=sys.argv)

print(f'\nPrompt tokens: {gemini_response.usage_metadata.prompt_token_count}\n')
print(f'Response tokens: {gemini_response.usage_metadata.candidates_token_count}\n')
print(f'Response:\n\n{gemini_response.text}')