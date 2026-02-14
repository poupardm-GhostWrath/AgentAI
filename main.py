import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

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

    # prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Response from Gemini Client
    response = client.models.generate_content(
        model=model_name, 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0),
        )
    if response.usage_metadata == None : raise RuntimeError("Failed API request")

    # Output from Response
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
