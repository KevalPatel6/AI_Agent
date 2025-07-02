import os 
from google.genai import types

def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    print(working_directory)

    if directory is not None:
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        print(full_path)
    else:
        full_path = working_directory
        print(full_path)

    #list directory items
    items = os.listdir(full_path)
    if len(items)==0:
        return f"There are no directories or files within this directory"       

    total_dir_contents = ""

    for item in items: 
        item_path = os.path.join(full_path,item)
        #file size
        try:
            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                total_dir_contents += f'{item}: file_size={file_size}, is_dir={os.path.isdir(item_path)}\n'

        #directory size
        
            elif os.path.isdir(item_path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(item_path):
                    for filename in filenames: 
                        file_path = os.path.join(dirpath,filename)
                        try:
                            if not os.path.islink(file_path):
                                total_size+= os.path.getsize(file_path)
                        except Exception as e:
                            return f"Error: Failed to get the size of {file_path}"
                total_dir_contents += f'{item}: file_size={total_size}, is_dir={os.path.isdir(item_path)}\n'
        
        except Exception as e:
            return f"Error: Failed processing '{item_path}'"
    
    return total_dir_contents
    
                
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)        
        

