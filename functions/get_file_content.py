import os
from config import *
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read the contents of.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    wd_abs = os.path.abspath(working_directory).rstrip(os.sep)
    fp_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    if not fp_abs.startswith(wd_abs):
        return f'Error: Cannot read "{file_path}" as it is outside outside the permitted working directory'
    if not os.path.isfile(fp_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(fp_abs, "r") as f:
            contents = f.read()
            if len(contents) > MAX_CHARS:
                return contents[0:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents
    except Exception as e:
        return f'Error: {e}'