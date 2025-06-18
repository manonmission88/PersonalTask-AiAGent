import os 

def write_file(working_directory,file_path,content):
    try: 
        working_directory = os.path.abspath(working_directory)
        file_path =  os.path.abspath(os.path.join(working_directory,file_path))
        if not file_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        #write content to the file 
        with open(file_path,'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {str(e)}"
    