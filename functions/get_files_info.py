import os

def get_files_info(working_directory, directory=None):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        if directory:
            directory = os.path.abspath(os.path.join(working_directory, directory))
        else:
            directory = working_directory

        # Check if the directory is within the working directory
        if not directory.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the directory exists and is a directory
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'

        # List contents of the directory
        contents = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                contents.append(f'- {item}: file_size=128 bytes, is_dir=True')
            elif os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                contents.append(f'- {item}: file_size={file_size} bytes, is_dir=False')

        return "\n".join(contents)

    except Exception as e:
        return f"Error: {str(e)}"
