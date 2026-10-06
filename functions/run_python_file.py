import os.path
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute python files with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "path to the file, should be relative to the working directory.",
                },
                "args": {
                    "type": "array[string]",
                    "description": "The arguements required by the python file being run. each parameter is stored as an entry in an arrays of strings."
                },

            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = []) -> str:
    try:
        # Create normalized paths and verify validity of target
        working_dir_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_target = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        
        if not is_valid_target:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # build and create subprocess 
        command = ["python", file_path_abs]
        command.extend(args)
        completed_proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
        
        # Build and return result string
        response_strings = []
        if completed_proc.returncode != 0:
            response_strings.append(f"Process exited with code {completed_proc.returncode}")
        if completed_proc.stderr == "" and completed_proc == "":
            response_strings.append("No output produced")
        else: 
            response_strings.append(f"STDOUT: {completed_proc.stdout}") 
            response_strings.append(f"STDERR: {completed_proc.stderr}")
        
        return "\n".join(response_strings)

    except Exception as e:
        return f"Error: executing Python file: {e}"