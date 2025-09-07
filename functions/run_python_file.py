import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the python file to run.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to be passed to the specified python file. If not provided, runs the python file without any arguments."
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    elif isinstance(args, str):
        args = [args]
    wd_abs = os.path.abspath(working_directory).rstrip(os.sep)
    fp_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    if not fp_abs.startswith(wd_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside outside the permitted working directory'
    if not os.path.isfile(fp_abs):
        return f'Error: File "{file_path}" not found.'
    if not fp_abs.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        cmd = ["python3", fp_abs] + args
        result = subprocess.run(cmd, cwd=wd_abs, timeout=30, capture_output=True, text=True)
        output = f'STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'
        if result.returncode != 0:
            output += f'\nProcess exited with code {result.returncode}'
        return output
    except Exception as e:
        return f'Error: {e}'
    