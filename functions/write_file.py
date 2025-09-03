import os

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