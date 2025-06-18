import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from config import MAX_ITERATIONS
from prompt import system_prompt

def parse_args():
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
                    items=types.Schema(type=types.Type.STRING),
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

    available_functions = types.Tool(function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file,
    ])

    for i in range(MAX_ITERATIONS):
        if verbose:
            print(f"\n===== ITERATION {i+1} =====")

        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            )
        )

        if verbose:
            print_token_usage(response)

        # Add all candidate responses to messages
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Check if there's a function call to execute
        if response.function_calls:
            # Call each function and append results to messages
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                # Append the tool response to messages
                messages.append(function_call_result.parts[0])
            # Wait before next iteration to avoid rate limiting
            time.sleep(2)
        else:
            # No function calls means the model is done
            print("\n=== FINAL RESPONSE ===\n")
            print(response.text)
            break
    else:
        # Loop ended without finalizing
        print("\nMaximum iterations reached without completion.")

if __name__ == "__main__":
    main()
