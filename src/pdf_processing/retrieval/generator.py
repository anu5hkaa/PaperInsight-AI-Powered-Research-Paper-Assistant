import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from pathlib import Path

# generator.py lives at src/pdf_processing/retrieval/generator.py
# parents[0]=retrieval, [1]=pdf_processing, [2]=src, [3]=PROJECT_ROOT
PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file at the project "
        "root (next to /data and /src) containing: GEMINI_API_KEY=your_key"
    )

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(prompt, retries=3):

    for attempt in range(retries):

        try:

            response = model.generate_content(prompt)

            return response.text

        except Exception as e:

            print("\nGemini Error:")
            print(e)

            
            if "429" in str(e):

                wait_time = (attempt + 1) * 15

                print(
                    f"\nRetrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                break

    
    return None