"""
LLM Factory - Creates the appropriate LLM instance based on configuration
"""
from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from config.settings import (
    MODEL_PROVIDER, 
    ANTHROPIC_API_KEY, 
    GOOGLE_API_KEY, 
    OPENAI_API_KEY,
    CLAUDE_MODEL, 
    GEMINI_MODEL,
    OPENAI_MODEL
)


def create_llm(temperature: float = 0):
    """
    Create an LLM instance based on the configured provider.
    
    Args:
        temperature: Temperature for generation (0 = deterministic, 1 = creative)
        
    Returns:
        LLM instance (ChatAnthropic, ChatGoogleGenerativeAI, or ChatOpenAI)
        
    Raises:
        ValueError: If provider is not supported or API key is missing
    """
    if MODEL_PROVIDER == "claude":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set. Please set it in your .env file or environment.")
        
        return ChatAnthropic(
            model=CLAUDE_MODEL,
            temperature=temperature,
            api_key=ANTHROPIC_API_KEY
        )
    
    elif MODEL_PROVIDER == "gemini":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not set. Please set it in your .env file or environment.")
        
        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            temperature=temperature,
            google_api_key=GOOGLE_API_KEY
        )
    
    elif MODEL_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set. Please set it in your .env file or environment.")
        
        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
    
    else:
        raise ValueError(
            f"Unsupported MODEL_PROVIDER: {MODEL_PROVIDER}. "
            f"Supported providers: 'claude', 'gemini', 'openai'"
        )


def get_model_info():
    """
    Get information about the currently configured model.
    
    Returns:
        Dictionary with provider, model name, and API key status
    """
    if MODEL_PROVIDER == "claude":
        api_key_set = bool(ANTHROPIC_API_KEY)
        model_name = CLAUDE_MODEL
    elif MODEL_PROVIDER == "gemini":
        api_key_set = bool(GOOGLE_API_KEY)
        model_name = GEMINI_MODEL
    elif MODEL_PROVIDER == "openai":
        api_key_set = bool(OPENAI_API_KEY)
        model_name = OPENAI_MODEL
    else:
        api_key_set = False
        model_name = "unknown"
    
    return {
        "provider": MODEL_PROVIDER,
        "model": model_name,
        "api_key_set": api_key_set
    }

