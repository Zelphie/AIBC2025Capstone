# backend/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- OpenAI / LLM settings ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Please add it to your .env file.")

# --- Retirement sums (example; update to current official values) ---
CURRENT_YEAR_BRS = 106_500.0
CURRENT_YEAR_FRS = 213_000.0
CURRENT_YEAR_ERS = 426_000.0
CURRENT_YEAR_LABEL = "2025"  # update as needed

