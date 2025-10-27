"""
State filtering utilities for managing message history in the multi-agent system.
"""

from typing import Any, Dict, List
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, BaseMessage


def filter_tool_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    """
    Filter out ToolMessage objects from the message list while keeping AIMessages and HumanMessages.
    This allows the supervisor to see what tools were called but not the raw CSV data outputs.
    
    Args:
        messages: List of messages to filter
        
    Returns:
        Filtered list of messages without ToolMessage objects
    """
    filtered = []
    for msg in messages:
        if not isinstance(msg, ToolMessage):
            filtered.append(msg)
    return filtered


def create_worker_node(agent, agent_name: str):
    """
    Create a node function that wraps a worker agent and filters its output.
    
    The node function:
    1. Invokes the worker agent with the current state
    2. Filters out ToolMessage objects from the result
    3. Returns the filtered messages back to the supervisor
    
    Args:
        agent: The worker agent to wrap
        agent_name: Name of the agent for identification
        
    Returns:
        A node function that can be added to the graph
    """
    def node_function(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Node function that invokes the agent and filters tool messages.
        """
        # Invoke the agent with the current state
        result = agent.invoke(state)
        
        # Filter out ToolMessage objects to reduce token usage
        filtered_messages = filter_tool_messages(result["messages"])
        
        # Return the filtered messages
        return {"messages": filtered_messages}
    
    # Set the function name for better graph visualization
    node_function.__name__ = agent_name
    
    return node_function


def extract_delegation_message(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only the most recent message for delegation to a worker agent.
    This ensures workers only see what the supervisor explicitly delegated to them.
    
    Args:
        state: The current graph state
        
    Returns:
        State containing only the delegation message
    """
    messages = state.get("messages", [])
    if messages:
        # Return only the last message (the delegation from supervisor)
        return {"messages": [messages[-1]]}
    return {"messages": []}


def get_final_response(messages: List[BaseMessage]) -> str:
    """
    Extract the final response text from a list of messages.
    
    Args:
        messages: List of messages
        
    Returns:
        The content of the last AI message, or empty string if none found
    """
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content
    return ""


def summarize_agent_interaction(messages: List[BaseMessage], agent_name: str) -> str:
    """
    Create a summary of an agent's interaction including tools called and final response.
    Useful for creating concise handoff messages.
    
    Args:
        messages: List of messages from the agent interaction
        agent_name: Name of the agent
        
    Returns:
        A summary string
    """
    tool_calls = []
    final_response = ""
    
    for msg in messages:
        if isinstance(msg, AIMessage):
            # Check if this message has tool calls
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_calls.append(tool_call.get('name', 'unknown'))
            # Get the final content
            if msg.content:
                final_response = msg.content
    
    summary = f"{agent_name} completed analysis"
    if tool_calls:
        summary += f" (used tools: {', '.join(set(tool_calls))})"
    
    return summary

