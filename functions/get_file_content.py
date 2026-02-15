import os
from config import CHARACTER_LIMIT
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):

    # Set Absolute Path for File and Working Directory
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # Check Path is Valid
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if valid_target_file == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Check if target is a file
    if os.path.isfile(target_file) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Read the content of the target_file with a CHARACTER_LIMIT
    try:
        file_content = []
        file_object = open(target_file)
        file_content = file_object.read(CHARACTER_LIMIT)
        if file_object.read(1):
            file_content += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
    except Exception as e:
        return f"Error: {e}"
    return file_content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="List the content of a specified file relative to the working directory, truncated to a limited amount of characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list the content from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)