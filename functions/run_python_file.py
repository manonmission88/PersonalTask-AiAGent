import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        # Resolve absolute paths
        working_directory = os.path.abspath(working_directory)
        resolved_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if the file is within the working directory
        if not resolved_file_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if the file exists
        if not os.path.exists(resolved_file_path):
            return f'Error: File "{os.path.basename(file_path)}" not found.'

        # Check if the file is a Python file
        if not resolved_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the Python file using subprocess
        result = subprocess.run(
            ['python3', resolved_file_path],
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )

        # Format the output
        stdout = result.stdout.decode('utf-8').strip()
        stderr = result.stderr.decode('utf-8').strip()
        output = []

        if stdout:
            output.append(f"STDOUT:\n{stdout}")
        if stderr:
            output.append(f"STDERR:\n{stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not output:
            return "No output produced."

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
