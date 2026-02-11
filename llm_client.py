import google.generativeai as genai
from google.generativeai import types
import logging
from config import GEMINI_API_KEY, LLM_MODEL, EMBED_MODEL

logger = logging.getLogger("gucci_ai")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class LLMClient:
    def __init__(self):
        self.model = genai.GenerativeModel(LLM_MODEL)

    def embed_text(self, text: str):
        try:
            result = genai.embed_content(
                model=EMBED_MODEL,
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            raise e

    def generate_response(self, prompt: str):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "quota" in error_msg or "exhausted" in error_msg:
                return "The system is currently unavailable due to high traffic (Free Tier Limits). We are using the free version of Gemini for this project demonstration."
            logger.error(f"LLM Generation Error: {e}")
            return "I apologize, but I encountered an internal error processing your request."
