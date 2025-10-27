"""
Configuration settings for the Logistics Multi-Agent System
"""

import os
from pathlib import Path

# Project root directory (parent of config folder)
PROJECT_ROOT = Path(__file__).parent.parent

# Mock data directory
MOCK_DATA_DIR = PROJECT_ROOT / "mock_data"

# API Configuration
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Model Configuration
MODEL_NAME = "claude-sonnet-4-20250514"
# MODEL_NAME = "claude-3-5-sonnet-20241022"
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

