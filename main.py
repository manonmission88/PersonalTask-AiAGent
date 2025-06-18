import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

def parse_args():
    # Separate prompt parts and flags
    prompt_parts = []
    verbose = False
    for arg in sys.argv[1:]:
        if arg in ['--verbose', '-v']:
            verbose = True
        else:
            prompt_parts.append(arg)
    if not prompt_parts:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)
    prompt = " ".join(prompt_parts)
    return prompt, verbose

def print_token_usage(response):
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt, verbose = parse_args()
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    system_prompt = """You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists the files and folders in the specified directory, showing their size and type (file or folder).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Relative path to the target directory (within working directory).",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads and returns the content of a file within the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Relative path to the file to be read.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python script file within the working directory and returns its output.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Relative path to the Python file to execute.",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="Optional command-line arguments to pass to the Python script.",
                    items=types.Schema(type=types.Type.STRING)
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwrites the content of a file within the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Relative path to the file to write to.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write into the file.",
                ),
            },
        ),
    )
    #all available functions 
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file
        
    ]
)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents= messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
)
    )
    #check function calls 
    if response.function_calls:
        for function_call_part in response.function_calls:
            # print(json.loads(function_call_part))
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)
    if verbose:
        print(f"User prompt: {prompt}")
    print_token_usage(response)

if __name__ == "__main__":
    main()
