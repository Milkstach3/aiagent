import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

def main():
    verbose = False
    if sys.argv[-1] == "--verbose":
        sys.argv.pop()
        verbose = True

    if len(sys.argv) <= 1:
        print("Usage: python main.py <prompt>")
        return exit(1)
    
    
    
    

    user_prompt = " ".join(sys.argv[1:])
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]



    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages, 
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    function_call_part = response.function_calls if response.function_calls else None

    print(response.text)
    if function_call_part: print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if verbose:
        print("User prompt: " + user_prompt)
        print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
        print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

main()