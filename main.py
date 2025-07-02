import os 
from dotenv import load_dotenv
import sys
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
))

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if '--verbose' in sys.argv:
    print(f"User prompt: {user_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
elif len(response.function_calls)!=0:
    print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
else: print(response.text)

