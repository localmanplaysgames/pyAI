import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if sys.argv[1:] == []: # quit if nothing provided to pass into gemini
    sys.exit(1)

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

messages = [
    types.Content(role='user', parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages)

print(f'\nPrompt tokens: {gemini_response.usage_metadata.prompt_token_count}\n')
print(f'Response tokens: {gemini_response.usage_metadata.candidates_token_count}\n')
print(f'Response:\n\n{gemini_response.text}')