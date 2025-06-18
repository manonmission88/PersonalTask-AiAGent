import os
from config import MAX_CHARS
def get_file_content(working_directory, file_path):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the file is within the working directory
        if not file_path.startswith(working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists and is a file
        if not os.path.isfile(file_path):
            return f"Error: File not found or is not a regular file: {file_path}"

        # Read and return the file content
        #truncate the content 
        with open(file_path, 'r') as file:
            content = file.read()
            # print(len(content),"+++")
            if len(content) > MAX_CHARS:
                truncated_content = content[:MAX_CHARS] + f"\n[...File \"{file_path}\" truncated at 10000 characters]"
                return truncated_content
            return content
        
    except Exception as e:
        return f"Error: {str(e)}"


