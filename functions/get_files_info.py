import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if os.path.isfile(target_dir):
            return f'Error: "{directory}" is not a directory'
        if os.path.isdir(target_dir):
            return f'{build_info(target_dir)}'
    except Exception as e:
        return f"Error: {e}"

def build_info(target_dir: str) -> str:
    try:
        items = os.listdir(target_dir)
        res = []
        for item in items:
            # add name
            info = " - " + item + ": "
            # add size
            path = os.path.join(target_dir, item)
            info += "file_size=" + str(os.path.getsize(path)) + " bytes"
            # add is_dir=True/False
            if os.path.isdir(path):
                info += ", is_dir=True"
            else: 
                info += ", is_dir=False"
            res.append(info)
        return "\n".join(res) 

    except Exception as e:
        return f"Error: {e}"