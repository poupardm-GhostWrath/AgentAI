import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if valid_target_dir == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) == False:
        return f'Error: "{directory}" is not a directory'
    directory_content = []
    if directory == ".":
        directory_content.append("Result for current directory:")
    else:
        directory_content.append(f"Result for '{directory}' directory:")
    for item in os.listdir(target_dir):
        try:
            directory_content.append(f"- {item}: file_size={os.path.getsize(target_dir + "/"+ item)} bytes, is_dir={os.path.isdir(target_dir + "/"+ item)}")
        except Exception as e:
            return f"Error: {e}"
    return "\n".join(directory_content)