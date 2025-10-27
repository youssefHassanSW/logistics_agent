"""
Route Planner Agent - Specialized in logistics route optimization
"""

from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from config import MODEL_NAME, AGENT_NAMES
from tools import optimize_routes, assign_vehicle_to_route, check_traffic_conditions


def create_llm():
    """Create a Claude LLM instance"""
    return ChatAnthropic(model=MODEL_NAME, temperature=0)


route_planner_agent = create_agent(
    model=create_llm(),
    tools=[optimize_routes, assign_vehicle_to_route, check_traffic_conditions],
    system_prompt=(
        "You are a Route Planner agent specialized in logistics route optimization.\n\n"
        "RESPONSIBILITIES:\n"
        "- Analyze route efficiency and identify optimization opportunities\n"
        "- Evaluate traffic conditions and their impact on deliveries\n"
        "- Recommend vehicle assignments and route adjustments\n"
        "- Handle route disruptions and provide alternative routing solutions\n\n"
        "INSTRUCTIONS:\n"
        "- Use your tools to analyze route data from the provided scenario\n"
        "- Provide clear, actionable recommendations\n"
        "- Focus on minimizing delays and optimizing delivery times\n"
        "- Consider traffic conditions in all recommendations\n"
        "- Respond with a concise summary of findings and recommended actions\n"
        "- Do NOT include raw data dumps in your response\n"
    ),
    name=AGENT_NAMES["route_planner"],
)

