import os
from config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if valid_target_file == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(target_file) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        file_content = []
        file_object = open(target_file)
        file_content = file_object.read(CHARACTER_LIMIT)
        if file_object.read(1):
            file_content += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
    except Exception as e:
        return f"Error: {e}"
    return file_content