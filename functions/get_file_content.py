import os

def get_file_content(working_directory, file_path):
    working_dir_path = os.path.abspath(working_directory)
    print(working_dir_path)
    file_full_path = os.path.abspath(os.path.join(working_dir_path, file_path))
    print(file_full_path)
    if not file_full_path.startswith(working_dir_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000
    
    try:
        with open(file_full_path, "r") as f:
            full_content = f.read()
            if len(full_content)>MAX_CHARS:
                content = full_content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
                return content
            else: return full_content
    
    except Exception as e:
        return f"Error could not read file '{file_path}': {e}"