import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *

from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python_file import *

def main():

    verbose = '--verbose' in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != '--verbose']
    if not args:
        sys.exit(1)
    user_prompt = ' '.join(args)

    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    def call_function(function_call_part, verbose=False):
        if verbose:
            print (f'Calling function: {function_call_part.name}({function_call_part.args})')
        else:
            print (f' - Calling function: {function_call_part.name}')
        function_map = {
            'get_files_info': get_files_info,
            'get_file_content': get_file_content,
            'run_python_file': run_python_file,
            'write_file': write_file
        }
        func = function_map.get(function_call_part.name)
        if func:
            result =  func('./calculator', **function_call_part.args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={'result':result}
                    )
                ]
            )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )   

    messages = [
        types.Content(role='user', parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT))

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {prompt_tokens}')
        print(f'Response tokens: {response_tokens}')
    if response.function_calls != None and len(response.function_calls) > 0:
        function_call = call_function(response.function_calls[0])
        result = function_call.parts[0].function_response.response.get('result')
        if not result:
            raise Exception('FUNCTION CALL FAILED, TERMINATING.')
        else:
            if verbose:
                print(function_call.parts[0].function_response.response)
            else:
                print(result)

    else:
        print(f'Response: {response.text}')

if __name__ == '__main__':
    main()