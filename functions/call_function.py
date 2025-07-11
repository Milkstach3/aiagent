from google import genai
from google.genai import types
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .run_python import run_python_file
from .write_file import write_file

# from google.genai import types

# from functions.get_files_info import get_files_info, schema_get_files_info
# from functions.get_file_content import get_file_content, schema_get_file_content
# from functions.run_python import run_python_file, schema_run_python_file
# from functions.write_file_content import write_file, schema_write_file
# from config import WORKING_DIR

from schemas import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
)

# available_functions = types.Tool(
#     function_declarations=[
#         schema_get_files_info,
#         schema_get_file_content,
#         schema_run_python_file,
#         schema_write_file,
#     ]
# )

WORKING_DIR = "./calculator"

def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    # if verbose:
    #     print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    # else:
    #     print(f" - Calling function: {function_call_part.name}")
    
    # function_name = function_call_part.name
    # function_call_args = function_call_part.args
    # function_call_args['working_directory'] = './calculator'

    # results = None

    # if function_name == "get_file_content":
    #     results = get_file_content(function_call_args['working_directory'], function_call_args['file_path'])
        
    # elif function_name == "get_files_info":
    #     results = get_files_info(function_call_args['working_directory'], function_call_args.get('directory'))
        
    # elif function_name == 'run_python_file':
    #     results = run_python_file(function_call_args['working_directory'], function_call_args['file_path'])
        
    # elif function_name == 'write_file':
    #     results = write_file(function_call_args['working_directory'], function_call_args['file_path'], function_call_args['content'])
        
    # else:
    #     return types.Content(
    #         role="tool",
    #         parts=[
    #             types.Part.from_function_response(
    #                 name=function_name,
    #                 response={"error": f"Unknown function: {function_name}"},
    #             )
    #         ],
    #     )
    # return types.Content(
    #     role="tool",
    #     parts=[
    #         types.Part.from_function_response(
    #             name=function_name,
    #             response=results,
    #         )
    #     ],
    # )