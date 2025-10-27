"""
Distribution Handler Agent Tools
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
def detect_traffic_delays(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Detect traffic delays affecting deliveries and assess impact on SLAs.
    Reads deliveries.csv and traffic_incidents.csv to identify delay impacts.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        deliveries_df = pd.read_csv(scenario_path / "deliveries.csv")
        
        result = f"Traffic Delay Impact Analysis:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Total active deliveries: {len(deliveries_df)}\n"
        
        # Check for delayed deliveries
        if 'status' in deliveries_df.columns:
            delayed = deliveries_df[deliveries_df['status'].isin(['DELAYED', 'AT_RISK'])]
            
            if not delayed.empty:
                result += f"\n⚠️ Delayed deliveries: {len(delayed)}\n\n"
                
                for _, delivery in delayed.iterrows():
                    result += f"🚚 Delivery {delivery.get('delivery_id', 'N/A')}:\n"
                    result += f"   Status: {delivery.get('status', 'N/A')}\n"
                    
                    if 'customer_id' in delivery:
                        result += f"   Customer: {delivery['customer_id']}\n"
                    
                    if 'priority' in delivery:
                        result += f"   Priority: {delivery['priority']}\n"
                    
                    if 'delay_minutes' in delivery:
                        result += f"   Delay: {delivery['delay_minutes']} minutes\n"
                    
                    if 'sla_breach' in delivery and delivery['sla_breach']:
                        result += f"   🚨 SLA BREACH RISK\n"
                    
                    result += "\n"
        
        # Check traffic incidents
        incidents_path = scenario_path / "traffic_incidents.csv"
        if incidents_path.exists():
            incidents_df = pd.read_csv(incidents_path)
            result += f"Active traffic incidents: {len(incidents_df)}\n"
            
            if 'severity' in incidents_df.columns:
                critical = incidents_df[incidents_df['severity'].isin(['HIGH', 'CRITICAL'])]
                if not critical.empty:
                    result += f"Critical incidents: {len(critical)}\n"
        
        return result
        
    except Exception as e:
        return f"Error detecting traffic delays: {str(e)}"


@tool
def reroute_delivery(
    scenario_dir: Annotated[str, "Scenario directory name"],
    delivery_id: Annotated[str, "Delivery ID to reroute"]
) -> str:
    """
    Find and recommend alternative routes for a delivery.
    Reads alternative_routes.csv to provide rerouting options.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        deliveries_df = pd.read_csv(scenario_path / "deliveries.csv")
        
        # Find the delivery
        delivery = deliveries_df[deliveries_df['delivery_id'] == delivery_id]
        if delivery.empty:
            return f"Delivery {delivery_id} not found"
        
        delivery_info = delivery.iloc[0]
        
        result = f"Rerouting Options for Delivery {delivery_id}:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Current Status: {delivery_info.get('status', 'N/A')}\n"
        
        if 'current_route' in delivery_info:
            result += f"Current Route: {delivery_info['current_route']}\n"
        
        if 'destination' in delivery_info:
            result += f"Destination: {delivery_info['destination']}\n"
        
        # Check for alternative routes
        alt_routes_path = scenario_path / "alternative_routes.csv"
        if alt_routes_path.exists():
            alt_routes_df = pd.read_csv(alt_routes_path)
            
            # Filter for this delivery if possible
            if 'delivery_id' in alt_routes_df.columns:
                relevant_routes = alt_routes_df[alt_routes_df['delivery_id'] == delivery_id]
            else:
                relevant_routes = alt_routes_df
            
            if not relevant_routes.empty:
                result += f"\nAvailable Alternative Routes: {len(relevant_routes)}\n\n"
                
                for idx, route in relevant_routes.iterrows():
                    result += f"🛣️ Option {idx + 1}:\n"
                    
                    if 'route_id' in route:
                        result += f"   Route ID: {route['route_id']}\n"
                    
                    if 'estimated_time' in route:
                        result += f"   Estimated Time: {route['estimated_time']} min\n"
                    
                    if 'distance_km' in route:
                        result += f"   Distance: {route['distance_km']} km\n"
                    
                    if 'feasibility_score' in route:
                        score = route['feasibility_score']
                        if score >= 0.8:
                            feasibility = "✓ High"
                        elif score >= 0.6:
                            feasibility = "⚡ Medium"
                        else:
                            feasibility = "⚠️ Low"
                        result += f"   Feasibility: {feasibility} ({score:.2f})\n"
                    
                    if 'traffic_conditions' in route:
                        result += f"   Traffic: {route['traffic_conditions']}\n"
                    
                    result += "\n"
            else:
                result += f"\n⚠️ No alternative routes available for this delivery\n"
        else:
            result += f"\n⚠️ No alternative routes data available\n"
        
        return result
        
    except Exception as e:
        return f"Error finding alternative routes: {str(e)}"


@tool
def get_upcoming_deliveries(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Get information about upcoming deliveries and their SLA requirements.
    Reads deliveries.csv and customer_sla.csv to assess delivery priorities.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        deliveries_df = pd.read_csv(scenario_path / "deliveries.csv")
        
        result = f"Upcoming Deliveries Overview:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Total deliveries: {len(deliveries_df)}\n"
        
        if 'status' in deliveries_df.columns:
            status_counts = deliveries_df['status'].value_counts()
            result += f"\nDelivery Status:\n{status_counts.to_string()}\n"
        
        # Priority deliveries
        if 'priority' in deliveries_df.columns:
            high_priority = deliveries_df[deliveries_df['priority'].isin(['HIGH', 'CRITICAL'])]
            
            if not high_priority.empty:
                result += f"\n🎯 High Priority Deliveries: {len(high_priority)}\n\n"
                
                for _, delivery in high_priority.head(10).iterrows():
                    result += f"📦 {delivery.get('delivery_id', 'N/A')}: "
                    result += f"{delivery.get('priority', 'N/A')} priority, "
                    result += f"Status: {delivery.get('status', 'N/A')}"
                    
                    if 'time_window_end' in delivery:
                        result += f", Due: {delivery['time_window_end']}"
                    
                    if 'sla_breach' in delivery and delivery['sla_breach']:
                        result += " 🚨 SLA BREACH"
                    
                    result += "\n"
        
        # SLA analysis
        sla_path = scenario_path / "customer_sla.csv"
        if sla_path.exists():
            sla_df = pd.read_csv(sla_path)
            
            result += f"\n📋 Customer SLA Summary:\n"
            result += f"Customers tracked: {len(sla_df)}\n"
            
            if 'sla_status' in sla_df.columns:
                breaches = sla_df[sla_df['sla_status'] == 'BREACH']
                if not breaches.empty:
                    result += f"\n🚨 SLA Breaches: {len(breaches)}\n"
                    
                    for _, customer in breaches.iterrows():
                        result += f"   • Customer {customer.get('customer_id', 'N/A')}: "
                        
                        if 'customer_tier' in customer:
                            result += f"{customer['customer_tier']} tier, "
                        
                        if 'penalty_amount' in customer:
                            result += f"Penalty: ${customer['penalty_amount']}"
                        
                        result += "\n"
        
        return result
        
    except Exception as e:
        return f"Error getting upcoming deliveries: {str(e)}"

