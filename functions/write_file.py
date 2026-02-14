import os

def write_file(working_directory, file_path, content):

    # Set Absolute Path for File and Working Directory
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Check Path is Valid
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if valid_target_file == False:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Check if Path is a directory
    if os.path.isdir(target_file) == True:
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # Check if parent directories exist. Make them if necessary
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    except Exception as e:
        return f'Error: {e}'
    
    # Open File in write mode
    try:
        file_object = open(target_file, mode="w")
        amount_wrote = file_object.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    pass