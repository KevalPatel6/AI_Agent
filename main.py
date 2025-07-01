import os 
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if '--verbose' in sys.argv:
    print(f"User prompt: {user_prompt}\nPrompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
else: print(response.text)
