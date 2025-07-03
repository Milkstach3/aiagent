import os
import sys
from google import genai
from google.genai import types
from main import system_prompt

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)



def get_files_info(working_directory, directory=None):
    # Build and return a string representing the contents of the directory. It should use this format:
    # - <filename>: file_size=<size> bytes, is_dir=<True/False>
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False

    
    # print("Started trying")
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = abs_working_dir

    # If there is a directory specified. That is, if directory is not None.
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    
    # This line checks if the target directory starts with the string of the absolute working directory, which by definition prevents directory traversal attacks.
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # This line checks if the target directory is a valid directory.
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    

 
    try:    
        # files_info is where we will store the information about each file
        files_info = []
        # os.listdir returns an iterable list of the files in the directory. filename is an individual file.
        for filename in os.listdir(target_dir):
            # filepath is value passed to isdir and getsize. Joining target_dir and filename puts the value in the correct format.
            filepath = os.path.join(target_dir, filename)
            # Initialize file_size to 0 so Python knows it's an integer.
            file_size = 0
            # Check if the filepath is a directory or a file
            is_dir = os.path.isdir(filepath)
            # Get the file size.
            file_size = os.path.getsize(filepath)
            # Add the filename, file_size and is_dir to the formatted string, and add the formatted string to the end of the files_info array.
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        # Concatenate all the strings of files_info into a single string with newlines.
        return "\n".join(files_info)
    
        # os.path.abspath(): Get an absolute path from a relative path
        # os.path.join(): Join two paths together safely (handles slashes)
        # .startswith(): Check if a string starts with a substring
        # os.path.isdir(): Check if a path is a directory
        # os.listdir(): List the contents of a directory
        # os.path.getsize(): Get the size of a file
        # os.path.isfile(): Check if a path is a file
        # .join(): Join a list of strings together with a separator

    
    except Exception as e:
        return f"Error listing files: {e}"
    


