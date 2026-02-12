"""LLM initialization and utilities."""
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from src.config import LLM_PROVIDER, MODEL_NAME, OPENAI_API_KEY, ANTHROPIC_API_KEY


def get_llm(temperature: float = 0.7):
    """Initialize and return the LLM based on configuration."""
    
    if LLM_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return ChatOpenAI(
            model=MODEL_NAME,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
    elif LLM_PROVIDER == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        return ChatAnthropic(
            model=MODEL_NAME,
            temperature=temperature,
            api_key=ANTHROPIC_API_KEY
        )
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def create_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with variables."""
    return template.format(**kwargs)
