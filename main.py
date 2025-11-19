"""
Main entry point for the Logistics Multi-Agent System

This refactored version uses langgraph-supervisor for simplified supervisor/worker coordination.
"""

import os
from langchain_core.messages import HumanMessage
from langgraph_supervisor import create_supervisor

from config import MODEL_PROVIDER
from config.llm_factory import create_llm, get_model_info
from agents import (
    route_planner_agent,
    procurement_manager_agent,
    inventory_manager_agent,
    distribution_handler_agent,
    demand_forecaster_agent,
    cost_optimizer_agent,
)
from utils import load_scenario, list_available_scenarios

def create_logistics_graph():
    """
    Create the complete multi-agent logistics graph using langgraph-supervisor.
    
    Returns:
        Compiled supervisor graph ready for execution
    """
    llm = create_llm(temperature=0)
    
    # Create supervisor using the prebuilt langgraph-supervisor package
    supervisor = create_supervisor(
        model=llm,
        agents=[
            route_planner_agent,
            procurement_manager_agent,
            inventory_manager_agent,
            distribution_handler_agent,
            demand_forecaster_agent,
            cost_optimizer_agent,
        ],
        prompt=(
            "You are the Main Orchestrator for a logistics multi-agent system.\n\n"
            "ROLE:\n"
            "You coordinate specialized agents to handle logistics scenarios including:\n"
            "- Low inventory situations\n"
            "- Route disruptions and traffic issues\n"
            "- Demand spikes and forecasting\n"
            "- Cost optimization opportunities\n"
            "- Supplier issues and procurement\n"
            "- Distribution delays and SLA management\n\n"
            "AVAILABLE AGENTS:\n"
            "- Route Planner Agent\n"
            "- Procurement Manager Agent\n"
            "- Inventory Manager Agent\n"
            "- Distribution Handler Agent\n"
            "- Demand Forecaster Agent\n"
            "- Cost Optimizer Agent\n\n"
            "WORKFLOW:\n"
            "1. Analyze the trigger event and scenario data provided\n"
            "2. Determine which specialized agents need to be called\n"
            "3. Delegate tasks to agents ONE AT A TIME with clear instructions\n"
            "4. Review agent responses and delegate follow-up tasks if needed\n"
            "5. If the issue is not resolved, delegate the task to the next agent\n"
            "6. Synthesize a final natural language summary including:\n"
            "   - The issue that occurred\n"
            "   - Actions taken by each agent\n"
            "   - Overall recommendations and next steps: THIS SECTION MUST INCLUDE A FULLY DETAILED PLAN OF ACTION FOR THE NEXT STEPS\n\n"
            "INSTRUCTIONS:\n"
            "- When delegating, provide the agent with the scenario directory name and specific task\n"
            "- ALL AGENTS REQUIRED TO SOLVE THE ISSUE MUST BE CALLED BEFORE YOU CAN RETURN A SUMMARY\n"
            "- DO NOT RETURN ANY AGENT CALLS AS STEPS IN YOUR SUMMARY\n"
            "- When solving an issue, make sure to call all the necessary agents to solve the issue\n"
            "- Do NOT call multiple agents in parallel - delegate sequentially\n"
            "- Wait for each agent's response before deciding on next steps\n"
            "- The scenario directory follows the pattern: 'scenario_X_description'\n"
            "- After all agents have completed their work, provide a comprehensive summary\n"
            "- Your summary should be in natural language, suitable for management review\n"
            "- When listing anything in your summary, use markdown formatting and a newline delimeter after each item and section\n"
            "- Do NOT include raw data or tool outputs in your final summary\n"
            "- Focus on insights, actions taken, and business impact\n\n"
            "Remember: You are the coordinator. Do NOT perform the actual analysis yourself - "
            "delegate to the appropriate specialized agents using the transfer tools."
        ),
        add_handoff_back_messages=True,
        supervisor_name="Main_Orchestrator",  # No spaces for OpenAI compatibility
        output_mode="full_history",
    ).compile()
    
    return supervisor


def run_scenario(scenario_id: int, verbose: bool = True):
    """
    Run a specific scenario through the multi-agent system.
    
    Args:
        scenario_id: Scenario ID (1-6)
        verbose: If True, print detailed progress
        
    Returns:
        Final state after scenario execution
    """
    # Load the scenario
    scenario = load_scenario(scenario_id)
    if not scenario:
        print(f"Failed to load scenario {scenario_id}")
        return None
    
    if verbose:
        # Show model information
        model_info = get_model_info()
        
        print("\n" + "="*70)
        print(f"RUNNING SCENARIO {scenario_id}")
        print("="*70)
        print(f"Model: {model_info['provider'].upper()} - {model_info['model']}")
        print("="*70)
        if scenario['summary']:
            print(scenario['summary'])
        print("\n" + "-"*70)
        print("TRIGGER EVENT")
        print("-"*70)
        print(scenario['message'])
        print("\n" + "="*70)
        print("AGENT EXECUTION")
        print("="*70 + "\n")
    
    # Create the graph
    graph = create_logistics_graph()
    
    # Create initial state with the trigger message
    initial_state = {
        "messages": [HumanMessage(content=scenario['message'])]
    }
    
    # Run the graph
    final_state = None
    all_messages = []
    
    try:
        for step_num, state in enumerate(graph.stream(initial_state), 1):
            if verbose:
                # Print progress indicator with more detail
                node_name = list(state.keys())[0] if state else "unknown"
                print(f"\n[Step {step_num}] Processing node: {node_name}")
                
                # Show what messages were added in this step
                if state and node_name in state:
                    node_state = state[node_name]
                    if "messages" in node_state:
                        messages = node_state["messages"]
                        if messages:
                            latest_msg = messages[-1]
                            if hasattr(latest_msg, 'content') and latest_msg.content:
                                # Handle both string and list content (Gemini returns list)
                                content = latest_msg.content
                                if isinstance(content, list):
                                    # Extract text from list format (Gemini)
                                    content = ' '.join([str(item) if isinstance(item, str) else item.get('text', '') 
                                                       for item in content if item])
                                
                                # Show first 200 chars of the message
                                content_str = str(content)
                                content_preview = content_str[:200]
                                if len(content_str) > 200:
                                    content_preview += "..."
                                print(f"  Message: {content_preview}")
                                
                                # Collect all messages for final display
                                all_messages.append({
                                    'step': step_num,
                                    'node': node_name,
                                    'content': content_str
                                })
            
            final_state = state
        
        if verbose and final_state:
            print("\n" + "="*70)
            print("FINAL SUMMARY")
            print("="*70 + "\n")
            
            # langgraph-supervisor stores final state differently
            # Try multiple extraction methods
            summary_found = False
            
            # Method 1: Check the last state's messages
            if final_state:
                last_key = list(final_state.keys())[-1]
                if "messages" in final_state[last_key]:
                    messages = final_state[last_key]["messages"]
                    # Find the last AI message from supervisor
                    for msg in reversed(messages):
                        if hasattr(msg, 'content') and msg.content:
                            # Handle both string and list content (Gemini returns list)
                            content = msg.content
                            if isinstance(content, list):
                                # Extract text from list format (Gemini)
                                content = ' '.join([str(item) if isinstance(item, str) else item.get('text', '') 
                                                   for item in content if item])
                            content_str = str(content).strip()
                            
                            # Check if this is a substantial response (not just a tool call)
                            if len(content_str) > 50:
                                print(content_str)
                                summary_found = True
                                break
            
            # Method 2: If nothing found, show all collected messages
            if not summary_found and all_messages:
                print("=== AGENT INTERACTIONS ===\n")
                for msg_info in all_messages:
                    print(f"\n[{msg_info['step']}] {msg_info['node']}:")
                    print("-" * 70)
                    print(msg_info['content'])
                    print()
            
            if not summary_found and not all_messages:
                print("[No summary generated - check if supervisor completed successfully]")
            
            print("\n" + "="*70 + "\n")
    
    except Exception as e:
        print(f"\n[ERROR] Error during scenario execution: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    return final_state


def visualize_graph(output_path: str = "logistics_graph.png"):
    """
    Generate a visualization of the multi-agent graph.
    
    Args:
        output_path: Path to save the visualization
    """
    try:
        graph = create_logistics_graph()
        png_data = graph.get_graph().draw_mermaid_png()
        
        with open(output_path, "wb") as f:
            f.write(png_data)
        
        print(f"[OK] Graph visualization saved to {output_path}")
        
    except Exception as e:
        print(f"Error generating visualization: {e}")


def interactive_mode():
    """
    Interactive mode for running scenarios.
    """
    print("\n" + "="*70)
    print("LOGISTICS MULTI-AGENT SYSTEM - INTERACTIVE MODE")
    print("="*70 + "\n")
    
    list_available_scenarios()
    
    while True:
        print("\n" + "-"*70)
        choice = input("\nEnter scenario ID (1-6), 'list' to see scenarios, or 'quit' to exit: ").strip().lower()
        
        if choice == 'quit':
            print("Exiting...")
            break
        
        if choice == 'list':
            list_available_scenarios()
            continue
        
        try:
            scenario_id = int(choice)
            if scenario_id < 1 or scenario_id > 6:
                print("Invalid scenario ID. Please enter a number between 1 and 6.")
                continue
            
            run_scenario(scenario_id, verbose=True)
            
        except ValueError:
            print("Invalid input. Please enter a number, 'list', or 'quit'.")


def main():
    """
    Main entry point.
    """
    import sys
    
    # Check for API key based on model provider
    model_info = get_model_info()
    
    if not model_info['api_key_set']:
        print(f"[ERROR] API key not set for {model_info['provider'].upper()}")
        print(f"\nCurrent model provider: {model_info['provider']}")
        print(f"Current model: {model_info['model']}")
        print("\nPlease set the appropriate API key:")
        
        if MODEL_PROVIDER == "claude":
            print("  Windows: set ANTHROPIC_API_KEY=your-key-here")
            print("  Linux/Mac: export ANTHROPIC_API_KEY=your-key-here")
            print("  Or add to .streamlit/secrets.toml: ANTHROPIC_API_KEY = \"your-key-here\"")
        elif MODEL_PROVIDER == "gemini":
            print("  Windows: set GOOGLE_API_KEY=your-key-here")
            print("  Linux/Mac: export GOOGLE_API_KEY=your-key-here")
            print("  Or add to .streamlit/secrets.toml: GOOGLE_API_KEY = \"your-key-here\"")
        elif MODEL_PROVIDER == "openai":
            print("  Windows: set OPENAI_API_KEY=your-key-here")
            print("  Linux/Mac: export OPENAI_API_KEY=your-key-here")
            print("  Or add to .streamlit/secrets.toml: OPENAI_API_KEY = \"your-key-here\"")
        
        print("\nTo switch model provider, set MODEL_PROVIDER environment variable:")
        print("  For Claude: set MODEL_PROVIDER=claude")
        print("  For Gemini: set MODEL_PROVIDER=gemini")
        print("  For OpenAI (GPT): set MODEL_PROVIDER=openai")
        
        sys.exit(1)
    
    # Display current model configuration
    print(f"\n[INFO] Using {model_info['provider'].upper()} model: {model_info['model']}\n")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            list_available_scenarios()
        
        elif command == "viz" or command == "visualize":
            output_path = sys.argv[2] if len(sys.argv) > 2 else "logistics_graph.png"
            visualize_graph(output_path)
        
        elif command.isdigit():
            scenario_id = int(command)
            run_scenario(scenario_id, verbose=True)
        
        elif command == "interactive":
            interactive_mode()
        
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python main.py [scenario_id]    - Run specific scenario")
            print("  python main.py list             - List all scenarios")
            print("  python main.py interactive      - Interactive mode")
            print("  python main.py viz [filename]   - Generate graph visualization")
    
    else:
        # No arguments - run interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
