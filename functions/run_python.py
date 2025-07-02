import os
import subprocess

def run_python_file(working_directory, file_path):
    working_dir_path = os.path.abspath(working_directory)
   
    full_file_path = os.path.abspath(os.path.join(working_directory,file_path))
   
    if not full_file_path.startswith(working_dir_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found'
    
    if not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    

    
    try: 
        result = subprocess.run(['python3', full_file_path],
                                cwd=working_dir_path, 
                                timeout=30,
                                capture_output=True,
                                check=True,
                                text=True)
            
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and not stderr:
            return "No output produced"
        else: 
            return f'STDOUT: {stdout}\n',f'STDERR: {stderr}\n'
        
    except subprocess.CalledProcessError as e:
            if not e.stdout.strip():
                return "No output produced" 
            else:
                return (
                    f'Error: Process exited with code {e.returncode}\n')
        
    except subprocess.TimeoutExpired:
        return f'Error: Execution timed out after 30 seconds'
    except Exception as e:
        return f'Error: Unexpected exception error occurred: {e}'