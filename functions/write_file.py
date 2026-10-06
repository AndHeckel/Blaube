import os.path
from os import makedirs

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes or overwrites given content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the file, should be relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to be written to the file given in file_path."
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:

        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not is_valid_target:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(working_dir_abs, exist_ok=True)
        with open(file_path_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"