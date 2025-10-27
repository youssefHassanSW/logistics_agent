"""
Tools package for logistics agents
"""

from .route_planner_tools import optimize_routes, assign_vehicle_to_route, check_traffic_conditions
from .procurement_tools import check_supplier_status, place_purchase_order, predict_supplier_delays
from .inventory_tools import check_stock_levels, predict_inventory_shortage, update_reorder_points
from .distribution_tools import detect_traffic_delays, reroute_delivery, get_upcoming_deliveries
from .forecaster_tools import predict_demand_spike, get_demand_forecast, analyze_historical_trends
from .cost_optimizer_tools import analyze_financial_costs, calculate_roi, identify_cost_savings

__all__ = [
    # Route Planner
    "optimize_routes",
    "assign_vehicle_to_route",
    "check_traffic_conditions",
    # Procurement Manager
    "check_supplier_status",
    "place_purchase_order",
    "predict_supplier_delays",
    # Inventory Manager
    "check_stock_levels",
    "predict_inventory_shortage",
    "update_reorder_points",
    # Distribution Handler
    "detect_traffic_delays",
    "reroute_delivery",
    "get_upcoming_deliveries",
    # Demand Forecaster
    "predict_demand_spike",
    "get_demand_forecast",
    "analyze_historical_trends",
    # Cost Optimizer
    "analyze_financial_costs",
    "calculate_roi",
    "identify_cost_savings",
]

