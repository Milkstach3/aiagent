import os
import sys
import subprocess
def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = abs_working_dir
    split_path = file_path.split(os.sep)
    relative_path = os.path.join(working_directory, file_path)

    if file_path:
        target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not split_path[-1].endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        captured_output = subprocess.run(['python', relative_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
        formatted_output = f'STDOUT:\n{captured_output.stdout.strip()}\nSTDERR:\n{captured_output.stderr.strip()}'
        if captured_output.returncode != 0:
            formatted_output = f'{formatted_output}Process exited with code {captured_output.returncode}'

        if not formatted_output.strip():
            formatted_output = 'No output produced.'

        return formatted_output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"