import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
    )
    print(response.text)
    if verbose:
        print(f"User prompt: {prompt}")
    print_token_usage(response)

if __name__ == "__main__":
    main()
