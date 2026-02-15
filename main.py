import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import *


def prompt_gemini(client, model_name, messages):
    return client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt, 
            temperature=0),
        )

def main():
    load_dotenv()

    # Get API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None : raise RuntimeError("Gemini API Key not found")

    # Get AI Model
    model_name = os.environ.get("GEMINI_MODEL")

    # Create Gemini Client
    client = genai.Client(api_key=api_key)

    # Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Loop

    for i in range(20):

        # Response from Gemini Client
        response = prompt_gemini(client, model_name, messages)
        if response.usage_metadata == None : raise RuntimeError("Failed API request")
        
        
        
        if response.candidates == None:
            raise Exception("Error: candidates list empty")
        
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Output from Response
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if len(function_call_result.parts) < 1:
                    raise Exception("Error: parts list empty")
                if function_call_result.parts[0].function_response == None:
                    raise Exception("Error: function response is None")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("Error: response is None")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results.append(function_call_result.parts[0])
                #print(f"Calling function: {function_call.name}({function_call.args})"
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(f"Final response:\n{response.text}")
            break

        if i == 19:
            print(f"Error: Max iterations has been reached")
            exit(1)
    


if __name__ == "__main__":
    main()
