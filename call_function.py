from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types
import json
from config import WORKING_DIR,MAX_ITERATIONS



def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    function_name = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name} with args: {args}")
    else:
        print(f" - Calling function: {function_name}")

    if not isinstance(args, dict):
        try:
            args = json.loads(args)
        except Exception as e:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Failed to parse arguments: {e}"}
                    )
                ]
            )

    # Add working_directory manually
    args["working_directory"] = WORKING_DIR

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )

    try:
        result = function_map[function_name](**args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Function raised an exception: {str(e)}"}
                )
            ]
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )
