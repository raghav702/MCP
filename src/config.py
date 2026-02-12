"""Configuration settings for the Research Assistant Agent."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to load from Streamlit secrets if available (for deployment)
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        for key in ['GOOGLE_API_KEY', 'TAVILY_API_KEY', 'DEBUG']:
            if key in st.secrets and not os.getenv(key):
                os.environ[key] = st.secrets[key]
except:
    pass

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default LLM provider (openai, anthropic, or google)
if OPENAI_API_KEY:
    LLM_PROVIDER = "openai"
    MODEL_NAME = "gpt-4-turbo-preview"
elif ANTHROPIC_API_KEY:
    LLM_PROVIDER = "anthropic"
    MODEL_NAME = "claude-3-sonnet-20240229"
elif GOOGLE_API_KEY:
    LLM_PROVIDER = "google"
    MODEL_NAME = "gemini-2.5-flash-lite"
else:
    LLM_PROVIDER = "openai"
    MODEL_NAME = "gpt-4-turbo-preview"

# Agent settings
MAX_SEARCH_RESULTS = 10
MAX_SOURCES_TO_FETCH = 3
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
