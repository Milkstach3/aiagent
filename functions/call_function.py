from google import genai
from google.genai import types
import get_file_content
import get_files_info
import run_python
import write_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_name = function_call_part.name
    function_call_args = function_call_part.args
    function_call_args['working_directory'] = './calculator'

    results = None

    if function_name == "get_file_content":
        results = get_file_content(function_call_args['working_directory'], function_call_args['file_path'])
        
    elif function_name == "get_files_info":
        results = get_files_info(function_call_args['working_directory'], function_call_args.get('directory'))
        
    elif function_name == 'run_python':
        results = run_python(function_call_args['working_directory'], function_call_args['file_path'])
        
    elif function_name == 'write_file':
        results = write_file(function_call_args['working_directory'], function_call_args['file_path'], function_call_args['content'])
        
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