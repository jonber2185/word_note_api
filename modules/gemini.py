import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_prompt(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_gemini_response(words: list) -> dict:
    system_instruction = load_prompt('gemini_system.txt')

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=str(words),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=8000,
            system_instruction=system_instruction
        )
    )

    return json.loads(response.text)
