import os

def get_files_info(working_directory, directory="."):
    wd_abs = os.path.abspath(working_directory).rstrip(os.sep)
    target_abs = os.path.abspath(os.path.join(working_directory, directory))
    wd_prefix = wd_abs + os.sep
    if not (target_abs == wd_abs or target_abs.startswith(wd_prefix)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_abs):
        return f'Error: "{directory}" is not a directory'
    results = []
    for item in os.listdir(target_abs):
        try:
            item_path = os.path.join(target_abs, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
        except Exception as e:
            return f'Error: {e}'
        results.append(f' - {item}: file_size={file_size} bytes, is_dir={is_dir}')
    return '\n'.join(results)