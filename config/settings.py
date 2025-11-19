"""
Configuration settings for the Logistics Multi-Agent System
"""

import os
from pathlib import Path

# Project root directory (parent of config folder)
PROJECT_ROOT = Path(__file__).parent.parent

# Mock data directory
MOCK_DATA_DIR = PROJECT_ROOT / "mock_data"


def get_secret(key: str, default: str = "") -> str:
    """
    Get a secret value from Streamlit secrets or environment variables.
    
    This function provides a unified interface for accessing secrets that works both
    in Streamlit apps (using st.secrets) and in standalone scripts (using os.environ).
    
    Args:
        key: The secret key to retrieve
        default: Default value if the secret is not found
        
    Returns:
        The secret value or the default
    """
    # Try to import streamlit and use st.secrets
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except (ImportError, FileNotFoundError, KeyError):
        pass
    
    # Fallback to environment variables
    return os.environ.get(key, default)


# API Configuration
ANTHROPIC_API_KEY = get_secret("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY", "")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY", "")

# Model Configuration
# Supported: "claude", "gemini", or "openai"
MODEL_PROVIDER = get_secret("MODEL_PROVIDER", "claude").lower()

# Claude Models
CLAUDE_MODEL = "claude-sonnet-4-20250514"
# CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# Gemini Models
GEMINI_MODEL = "gemini-2.5-flash"

# OpenAI Models
OPENAI_MODEL = "gpt-4o"  # GPT-4o (latest GPT-4 model)
# OPENAI_MODEL = "gpt-5-mini"  # GPT-5 mini (latest GPT-5 model)

# Get the appropriate model name based on provider
if MODEL_PROVIDER == "claude":
    MODEL_NAME = CLAUDE_MODEL
elif MODEL_PROVIDER == "gemini":
    MODEL_NAME = GEMINI_MODEL
elif MODEL_PROVIDER == "openai":
    MODEL_NAME = OPENAI_MODEL
else:
    MODEL_NAME = CLAUDE_MODEL  # Default fallback
# Scenario mapping
SCENARIO_DIRS = {
    1: "scenario_1_low_inventory",
    2: "scenario_2_route_disruption",
    3: "scenario_3_demand_spike",
    4: "scenario_4_cost_optimization",
    5: "scenario_5_supplier_issues",
    6: "scenario_6_distribution_delays",
}

# Agent names
AGENT_NAMES = {
    "route_planner": "route_planner",
    "procurement_manager": "procurement_manager",
    "inventory_manager": "inventory_manager",
    "distribution_handler": "distribution_handler",
    "demand_forecaster": "demand_forecaster",
    "cost_optimizer": "cost_optimizer",
}

