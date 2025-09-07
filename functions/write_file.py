import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to a file at the specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file."
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    wd_abs = os.path.abspath(working_directory).rstrip(os.sep)
    fp_abs = os.path.abspath(os.path.join(wd_abs, file_path))
    if not fp_abs.startswith(wd_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(fp_abs), exist_ok=True)
        with open(fp_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'