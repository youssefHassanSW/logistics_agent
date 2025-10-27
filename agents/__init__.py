"""
Agent definitions for the Logistics Multi-Agent System
"""

from .route_planner import route_planner_agent
from .procurement_manager import procurement_manager_agent
from .inventory_manager import inventory_manager_agent
from .distribution_handler import distribution_handler_agent
from .demand_forecaster import demand_forecaster_agent
from .cost_optimizer import cost_optimizer_agent

__all__ = [
    "route_planner_agent",
    "procurement_manager_agent",
    "inventory_manager_agent",
    "distribution_handler_agent",
    "demand_forecaster_agent",
    "cost_optimizer_agent",
]

