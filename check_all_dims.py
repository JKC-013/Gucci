import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models_to_test = [
    "models/embedding-001",
    "models/text-embedding-004",
    "models/text-embedding-001"
]

print("--- Starting Dimension Check ---", flush=True)

for model in models_to_test:
    print(f"\nTesting: {model}", flush=True)
    try:
        result = genai.embed_content(
            model=model,
            content="Hello world",
            task_type="retrieval_query"
        )
        if 'embedding' in result:
             print(f"SUCCESS. Dimension: {len(result['embedding'])}", flush=True)
        else:
             print("SUCCESS but no embedding field?", flush=True)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)

print("\n--- End Check ---", flush=True)
