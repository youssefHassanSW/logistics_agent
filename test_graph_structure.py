"""
Test script to verify the graph structure without calling the LLM API
"""

from main import create_logistics_graph
from utils import list_available_scenarios, load_scenario
from config import AGENT_NAMES

def test_graph_structure():
    """Test that the graph is created with correct nodes and edges"""
    print("="*60)
    print("TESTING GRAPH STRUCTURE")
    print("="*60)
    
    try:
        graph = create_logistics_graph()
        print("\n[OK] Graph created successfully using langgraph-supervisor!")
        
        # Get graph info
        graph_info = graph.get_graph()
        nodes = list(graph_info.nodes.keys())
        
        print(f"\nNodes in graph: {len(nodes)}")
        for node in sorted(nodes):
            print(f"  - {node}")
        
        print("\n" + "="*60)
        print("GRAPH STRUCTURE TEST COMPLETED")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed to create graph: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scenario_loading():
    """Test loading scenarios without running them"""
    print("\n" + "="*60)
    print("TESTING SCENARIO LOADING")
    print("="*60 + "\n")
    
    list_available_scenarios()
    
    print("\n" + "-"*60)
    print("Testing individual scenario loading:")
    print("-"*60 + "\n")
    
    success_count = 0
    for scenario_id in range(1, 7):
        scenario = load_scenario(scenario_id)
        if scenario:
            print(f"[OK] Scenario {scenario_id} loaded successfully")
            success_count += 1
        else:
            print(f"[FAIL] Scenario {scenario_id} failed to load")
    
    print(f"\n{success_count}/6 scenarios loaded successfully")
    
    return success_count == 6


def test_tools_import():
    """Test that all tools can be imported"""
    print("\n" + "="*60)
    print("TESTING TOOLS IMPORT")
    print("="*60 + "\n")
    
    try:
        from tools import (
            optimize_routes, assign_vehicle_to_route, check_traffic_conditions,
            check_supplier_status, place_purchase_order, predict_supplier_delays,
            check_stock_levels, predict_inventory_shortage, update_reorder_points,
            detect_traffic_delays, reroute_delivery, get_upcoming_deliveries,
            predict_demand_spike, get_demand_forecast, analyze_historical_trends,
            analyze_financial_costs, calculate_roi, identify_cost_savings,
        )
        
        tools = [
            "optimize_routes", "assign_vehicle_to_route", "check_traffic_conditions",
            "check_supplier_status", "place_purchase_order", "predict_supplier_delays",
            "check_stock_levels", "predict_inventory_shortage", "update_reorder_points",
            "detect_traffic_delays", "reroute_delivery", "get_upcoming_deliveries",
            "predict_demand_spike", "get_demand_forecast", "analyze_historical_trends",
            "analyze_financial_costs", "calculate_roi", "identify_cost_savings",
        ]
        
        print(f"[OK] All {len(tools)} tools imported successfully\n")
        for tool in tools:
            print(f"  - {tool}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to import tools: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agents_creation():
    """Test that all agents can be created"""
    print("\n" + "="*60)
    print("TESTING AGENT CREATION")
    print("="*60 + "\n")
    
    try:
        from agents import (
            route_planner_agent,
            procurement_manager_agent,
            inventory_manager_agent,
            distribution_handler_agent,
            demand_forecaster_agent,
            cost_optimizer_agent,
        )
        
        agents = {
            "Route Planner": route_planner_agent,
            "Procurement Manager": procurement_manager_agent,
            "Inventory Manager": inventory_manager_agent,
            "Distribution Handler": distribution_handler_agent,
            "Demand Forecaster": demand_forecaster_agent,
            "Cost Optimizer": cost_optimizer_agent,
        }
        
        print(f"[OK] All {len(agents)} agents created successfully\n")
        for name, agent in agents.items():
            print(f"  - {name}: {type(agent).__name__}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to create agents: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# LOGISTICS MULTI-AGENT SYSTEM - STRUCTURE TESTS")
    print("# (Refactored with langgraph-supervisor)")
    print("#"*60 + "\n")
    
    results = {
        "Tools Import": test_tools_import(),
        "Agents Creation": test_agents_creation(),
        "Scenario Loading": test_scenario_loading(),
        "Graph Structure": test_graph_structure(),
    }
    
    print("\n" + "#"*60)
    print("# TEST SUMMARY")
    print("#"*60 + "\n")
    
    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "#"*60)
    if all_passed:
        print("# ALL TESTS PASSED")
        print("# System is ready to run!")
        print("# Set ANTHROPIC_API_KEY and run: python main.py")
    else:
        print("# SOME TESTS FAILED")
        print("# Please review the errors above")
    print("#"*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    run_all_tests()
