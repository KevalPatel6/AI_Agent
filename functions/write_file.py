import os

def write_file(working_directory, file_path, content):
    working_directory_path = os.path.abspath(working_directory)
    
    full_file_path = os.path.abspath(os.path.join(working_directory,file_path))

    if not full_file_path.startswith(working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(full_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(f'Error: There was an error making the filepath "{file_path}": {e}')
    