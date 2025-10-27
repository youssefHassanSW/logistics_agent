"""
Route Planner Agent Tools
"""

import pandas as pd
from pathlib import Path
from typing import Annotated
from langchain_core.tools import tool
from config import MOCK_DATA_DIR


def _get_scenario_path(scenario_dir: str) -> Path:
    """Helper to get scenario directory path"""
    return MOCK_DATA_DIR / scenario_dir


@tool
def optimize_routes(scenario_dir: Annotated[str, "Scenario directory name (e.g., 'scenario_2_route_disruption')"]) -> str:
    """
    Optimize routes based on current traffic conditions and vehicle availability.
    Reads routes.csv, vehicles.csv, and traffic_data.csv to provide route optimization recommendations.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        routes_df = pd.read_csv(scenario_path / "routes.csv")
        
        # Check if vehicles.csv exists
        vehicles_path = scenario_path / "vehicles.csv"
        if vehicles_path.exists():
            vehicles_df = pd.read_csv(vehicles_path)
        else:
            vehicles_df = None
            
        # Check if traffic_data.csv exists
        traffic_path = scenario_path / "traffic_data.csv"
        if traffic_path.exists():
            traffic_df = pd.read_csv(traffic_path)
        else:
            traffic_df = None
        
        result = f"Route Optimization Analysis:\n"
        result += f"Total routes: {len(routes_df)}\n"
        
        if 'status' in routes_df.columns:
            status_counts = routes_df['status'].value_counts()
            result += f"\nRoute Status Distribution:\n{status_counts.to_string()}\n"
            
            # Identify problematic routes
            problem_statuses = ['DELAYED', 'BLOCKED', 'REROUTE_NEEDED']
            problem_routes = routes_df[routes_df['status'].isin(problem_statuses)]
            
            if not problem_routes.empty:
                result += f"\n⚠️ Routes requiring attention: {len(problem_routes)}\n"
                for _, route in problem_routes.iterrows():
                    result += f"  - Route {route.get('route_id', 'N/A')}: {route.get('status', 'N/A')}"
                    if 'delay_minutes' in route:
                        result += f" (Delay: {route['delay_minutes']} min)"
                    result += "\n"
        
        if vehicles_df is not None and 'status' in vehicles_df.columns:
            available_vehicles = vehicles_df[vehicles_df['status'] == 'AVAILABLE']
            result += f"\nAvailable vehicles for reassignment: {len(available_vehicles)}\n"
        
        if traffic_df is not None:
            result += f"\nTraffic incidents affecting routes: {len(traffic_df)}\n"
        
        return result
        
    except Exception as e:
        return f"Error optimizing routes: {str(e)}"


@tool
def assign_vehicle_to_route(
    scenario_dir: Annotated[str, "Scenario directory name"],
    vehicle_id: Annotated[str, "Vehicle ID to assign"],
    route_id: Annotated[str, "Route ID to assign vehicle to"]
) -> str:
    """
    Assign a vehicle to a specific route. Updates vehicle assignments based on availability and route requirements.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        vehicles_df = pd.read_csv(scenario_path / "vehicles.csv")
        routes_df = pd.read_csv(scenario_path / "routes.csv")
        
        # Find the vehicle
        vehicle = vehicles_df[vehicles_df['vehicle_id'] == vehicle_id]
        if vehicle.empty:
            return f"Vehicle {vehicle_id} not found"
        
        vehicle_info = vehicle.iloc[0]
        
        # Find the route
        route = routes_df[routes_df['route_id'] == route_id]
        if route.empty:
            return f"Route {route_id} not found"
        
        route_info = route.iloc[0]
        
        # Check vehicle status
        if vehicle_info.get('status') not in ['AVAILABLE', 'EN_ROUTE']:
            return f"⚠️ Vehicle {vehicle_id} is {vehicle_info.get('status')} and may not be suitable for immediate assignment"
        
        result = f"✓ Vehicle Assignment Recommendation:\n"
        result += f"  Vehicle: {vehicle_id} ({vehicle_info.get('type', 'N/A')})\n"
        result += f"  Current Status: {vehicle_info.get('status', 'N/A')}\n"
        result += f"  Location: {vehicle_info.get('current_location', 'N/A')}\n"
        result += f"  Route: {route_id}\n"
        result += f"  Route Status: {route_info.get('status', 'N/A')}\n"
        
        if 'capacity' in vehicle_info and 'estimated_load' in route_info:
            if vehicle_info['capacity'] >= route_info['estimated_load']:
                result += f"  Capacity Check: ✓ Sufficient ({vehicle_info['capacity']} >= {route_info['estimated_load']})\n"
            else:
                result += f"  Capacity Check: ⚠️ Insufficient ({vehicle_info['capacity']} < {route_info['estimated_load']})\n"
        
        return result
        
    except Exception as e:
        return f"Error assigning vehicle: {str(e)}"


@tool
def check_traffic_conditions(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Check current traffic conditions and incidents affecting routes.
    Reads traffic_data.csv and traffic_incidents.csv to identify delays and disruptions.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        result = "Traffic Conditions Analysis:\n"
        
        # Check for traffic_data.csv
        traffic_data_path = scenario_path / "traffic_data.csv"
        if traffic_data_path.exists():
            traffic_df = pd.read_csv(traffic_data_path)
            result += f"\nTraffic Data Points: {len(traffic_df)}\n"
            
            if 'route_id' in traffic_df.columns and 'delay_minutes' in traffic_df.columns:
                total_delay = traffic_df['delay_minutes'].sum()
                avg_delay = traffic_df['delay_minutes'].mean()
                result += f"Total delay across all routes: {total_delay} minutes\n"
                result += f"Average delay per route: {avg_delay:.1f} minutes\n"
        
        # Check for traffic_incidents.csv
        incidents_path = scenario_path / "traffic_incidents.csv"
        if incidents_path.exists():
            incidents_df = pd.read_csv(incidents_path)
            result += f"\n⚠️ Active Traffic Incidents: {len(incidents_df)}\n"
            
            if 'severity' in incidents_df.columns:
                severity_counts = incidents_df['severity'].value_counts()
                result += f"\nIncident Severity:\n{severity_counts.to_string()}\n"
            
            # List critical incidents
            if 'severity' in incidents_df.columns:
                critical = incidents_df[incidents_df['severity'].isin(['HIGH', 'CRITICAL'])]
                if not critical.empty:
                    result += f"\n🚨 Critical Incidents:\n"
                    for _, incident in critical.head(5).iterrows():
                        result += f"  - {incident.get('incident_type', 'N/A')} on Route {incident.get('affected_route', 'N/A')}"
                        if 'estimated_delay' in incident:
                            result += f" (Est. delay: {incident['estimated_delay']} min)"
                        result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error checking traffic conditions: {str(e)}"

