import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Embedding Config
EMBED_MODEL = "models/gemini-embedding-001"
EMBED_DIM = 3072 # gemini-embedding-001 output dimension

# LLM Config
LLM_MODEL = "gemini-2.5-flash-lite" # Or gemini-1.5-flash
