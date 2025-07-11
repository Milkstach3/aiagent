import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from VARIABLES import SYSTEM_PROMPT, MAX_ITERS
from schemas import available_functions
from functions.call_function import call_function

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    final_response = generate_content(client, messages, verbose)
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"{final_response}")  
                break
        except Exception as e:
            print(f"Error during content generation: {e}")
            if verbose:
                print("Current messages:", messages)
            
           


    
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    # messages_updated.extend(function_responses)
    for cand in response.candidates:
        messages.append(cand.content)

    messages.append( types.Content( parts=function_responses, role="tool" ) )

    # return response.text, types.Content(
    #     parts=function_responses,
    #     role="tool",
    # )
    # return types.Content(
    #     parts=function_responses,
    #     role="tool",
    # )



if __name__ == "__main__":
    main()





    
    # verbose = False
    # if sys.argv[-1] == "--verbose":
    #     sys.argv.pop()
    #     verbose = True

    # if len(sys.argv) <= 1:
    #     print("Usage: python main.py <prompt>")
    #     return exit(1)

    # user_prompt = " ".join(sys.argv[1:])
    # load_dotenv()
    # api_key = os.environ.get("GEMINI_API_KEY")

    # client = genai.Client(api_key=api_key)

    # messages = [
    #     types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    # ]

    # # if verbose:
    # #     print("User prompt: " + user_prompt)
    # #     print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
    # #     print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

    
    # generate_content(client, messages, verbose)
    # generate_content(client, messages, verbose, user_prompt)

# def generate_content(client, messages, verbose=False, user_prompt=None):
#     response = client.models.generate_content(
#         model='gemini-2.0-flash-001', 
#         contents=messages, 
#         config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT),
#     )

#     # response_dict = {
#     #     'response': response,
#     #     'name': response.name
#     # }
#     # function_call_part = response.function_calls if response.function_calls else None

#     function_call_result = call_function(response.function_calls[0])
    
#     print(f"-> {function_call_result.parts[0].function_response.response}")

#     # print(response.text)
#     # if response.function_calls: print(f"Calling function: {response.function_calls}")

#     if verbose:
#         print("User prompt: " + user_prompt)
#         print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
#         print("Response tokens: " + str(response.usage_metadata.candidates_token_count))
#     return None
