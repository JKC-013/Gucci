import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = "models/gemini-embedding-001"

try:
    result = genai.embed_content(
        model=model,
        content="Hello world",
        task_type="retrieval_query"
    )
    print(f"Model: {model}")
    print(f"Dimension: {len(result['embedding'])}")
except Exception as e:
    print(f"Error: {e}")
