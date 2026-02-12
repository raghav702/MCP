"""Configuration settings for the Research Assistant Agent."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Default LLM provider (change to 'anthropic' if using Claude)
LLM_PROVIDER = "openai" if OPENAI_API_KEY else "anthropic"
MODEL_NAME = "gpt-4-turbo-preview" if LLM_PROVIDER == "openai" else "claude-3-sonnet-20240229"

# Agent settings
MAX_SEARCH_RESULTS = 10
MAX_SOURCES_TO_FETCH = 3
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
