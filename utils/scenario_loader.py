"""
Scenario Loader for the Logistics Multi-Agent System
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from config import MOCK_DATA_DIR, SCENARIO_DIRS


def load_trigger_event(scenario_id: int) -> Optional[Dict[str, Any]]:
    """
    Load the trigger event for a specific scenario.
    
    Args:
        scenario_id: Scenario ID (1-6)
        
    Returns:
        Dictionary containing trigger event data, or None if not found
    """
    if scenario_id not in SCENARIO_DIRS:
        print(f"Error: Invalid scenario ID {scenario_id}")
        return None
    
    scenario_dir = SCENARIO_DIRS[scenario_id]
    trigger_path = MOCK_DATA_DIR / scenario_dir / "trigger_event.csv"
    
    if not trigger_path.exists():
        print(f"Error: Trigger event file not found at {trigger_path}")
        return None
    
    try:
        trigger_df = pd.read_csv(trigger_path)
        
        if trigger_df.empty:
            print(f"Error: Trigger event file is empty")
            return None
        
        # Convert first row to dictionary
        trigger_event = trigger_df.iloc[0].to_dict()
        trigger_event['scenario_dir'] = scenario_dir
        trigger_event['scenario_id'] = scenario_id
        
        return trigger_event
        
    except Exception as e:
        print(f"Error loading trigger event: {e}")
        return None


def format_trigger_message(trigger_event: Dict[str, Any]) -> str:
    """
    Format the trigger event into a natural language message for the orchestrator.
    
    Args:
        trigger_event: Dictionary containing trigger event data
        
    Returns:
        Formatted message string
    """
    event_type = trigger_event.get('event_type', 'UNKNOWN')
    severity = trigger_event.get('severity', 'UNKNOWN')
    description = trigger_event.get('description', 'No description available')
    scenario_dir = trigger_event.get('scenario_dir', '')
    
    message = f"""
LOGISTICS SCENARIO ALERT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Event Type: {event_type}
Severity: {severity}
Scenario: {scenario_dir}

Description:
{description}

Please analyze this situation and coordinate the appropriate agents to handle it.
Provide a comprehensive response including:
1. Analysis of the issue
2. Actions taken by each consulted agent
3. Overall recommendations and next steps
"""
    
    return message.strip()


def get_scenario_summary(scenario_id: int) -> Optional[str]:
    """
    Get a brief summary of a scenario from scenario_index.csv.
    
    Args:
        scenario_id: Scenario ID (1-6)
        
    Returns:
        Summary string, or None if not found
    """
    index_path = MOCK_DATA_DIR / "scenario_index.csv"
    
    if not index_path.exists():
        return None
    
    try:
        index_df = pd.read_csv(index_path)
        scenario = index_df[index_df['scenario_id'] == scenario_id]
        
        if scenario.empty:
            return None
        
        scenario_data = scenario.iloc[0]
        
        summary = f"""
Scenario {scenario_id}: {scenario_data.get('scenario_name', 'Unknown')}
Complexity: {scenario_data.get('complexity', 'N/A')}
Severity: {scenario_data.get('severity', 'N/A')}
Primary Agents: {scenario_data.get('primary_agents', 'N/A')}
Key Metrics: {scenario_data.get('key_metrics', 'N/A')}
"""
        return summary.strip()
        
    except Exception as e:
        print(f"Error loading scenario summary: {e}")
        return None


def list_available_scenarios():
    """
    List all available scenarios with their basic information.
    """
    print("\n" + "="*60)
    print("AVAILABLE SCENARIOS")
    print("="*60 + "\n")
    
    index_path = MOCK_DATA_DIR / "scenario_index.csv"
    
    if not index_path.exists():
        print("Scenario index not found")
        return
    
    try:
        index_df = pd.read_csv(index_path)
        
        for _, scenario in index_df.iterrows():
            scenario_id = scenario.get('scenario_id')
            name = scenario.get('scenario_name', 'Unknown')
            severity = scenario.get('severity', 'N/A')
            complexity = scenario.get('complexity', 'N/A')
            
            print(f"[{scenario_id}] {name}")
            print(f"    Severity: {severity} | Complexity: {complexity}")
            print()
            
    except Exception as e:
        print(f"Error listing scenarios: {e}")


def validate_scenario_data(scenario_id: int) -> bool:
    """
    Validate that required data files exist for a scenario.
    
    Args:
        scenario_id: Scenario ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if scenario_id not in SCENARIO_DIRS:
        print(f"Invalid scenario ID: {scenario_id}")
        return False
    
    scenario_dir = SCENARIO_DIRS[scenario_id]
    scenario_path = MOCK_DATA_DIR / scenario_dir
    
    if not scenario_path.exists():
        print(f"Scenario directory not found: {scenario_path}")
        return False
    
    # Check for trigger_event.csv (required)
    trigger_path = scenario_path / "trigger_event.csv"
    if not trigger_path.exists():
        print(f"Missing trigger_event.csv in {scenario_dir}")
        return False
    
    print(f"[OK] Scenario {scenario_id} validated successfully")
    return True


def load_scenario(scenario_id: int) -> Optional[Dict[str, Any]]:
    """
    Load a complete scenario including trigger event and formatted message.
    
    Args:
        scenario_id: Scenario ID (1-6)
        
    Returns:
        Dictionary with scenario data including:
        - trigger_event: Raw trigger event data
        - message: Formatted message for orchestrator
        - scenario_dir: Directory name
        - summary: Scenario summary
    """
    # Validate scenario
    if not validate_scenario_data(scenario_id):
        return None
    
    # Load trigger event
    trigger_event = load_trigger_event(scenario_id)
    if not trigger_event:
        return None
    
    # Format message
    message = format_trigger_message(trigger_event)
    
    # Get summary
    summary = get_scenario_summary(scenario_id)
    
    return {
        'scenario_id': scenario_id,
        'scenario_dir': trigger_event['scenario_dir'],
        'trigger_event': trigger_event,
        'message': message,
        'summary': summary,
    }


if __name__ == "__main__":
    # Test the scenario loader
    list_available_scenarios()
    
    print("\n" + "="*60)
    print("TESTING SCENARIO LOADER")
    print("="*60 + "\n")
    
    # Test loading scenario 1
    scenario = load_scenario(1)
    if scenario:
        print("Scenario loaded successfully!")
        print("\nFormatted Message:")
        print(scenario['message'])

