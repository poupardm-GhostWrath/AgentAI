import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()

    # Get API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None : raise RuntimeError("Gemini API Key not found")

    # Create Gemini Client
    client = genai.Client(api_key=api_key)

    # Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    print(f"User prompt: {prompt}")

    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
    if response.usage_metadata == None : raise RuntimeError("Failed API request")

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
