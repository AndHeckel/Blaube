import os.path

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a singular file up.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the individual file, should be relative to the working directory.",
                },
            },
        },
    },
}

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        
        if not is_valid_target:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[....File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
            
    except Exception as e:
        return f"Error: {e}"