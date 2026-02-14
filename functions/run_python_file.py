import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    # Set Absolute Path for File and Working Directory
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

     # Check Path is Valid
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if valid_target_file == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if target is a file
    if os.path.isfile(target_file) == False:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    # Check if file end with .py
    if file_path.endswith("py") == False:
        return f'Error: "{file_path}" is not a Python file'
    
    # Create command for subprocess    
    command = ["python", target_file]

    # Check if additional args need to be added to command
    if args != None:
        command.extend(args)

    # Run subprocess
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    # Check output
    result_str = ""
    try:
        if result.check_returncode():
            result_str += f"Process exited with code {result.check_returncode()}"
        if result.stderr == None or result.stdout == None:
            result_str += f"No output produced"
        if result.stderr != None and result.stdout != None:
            result_str += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"
    return result_str