"""
Distribution Handler Agent - Specialized in delivery management and logistics
"""

from langchain.agents import create_agent
from config import AGENT_NAMES
from config.llm_factory import create_llm
from tools import detect_traffic_delays, reroute_delivery, get_upcoming_deliveries


distribution_handler_agent = create_agent(
    model=create_llm(),
    tools=[detect_traffic_delays, reroute_delivery, get_upcoming_deliveries],
    system_prompt=(
        "You are a Distribution Handler agent specialized in delivery management and logistics.\n\n"
        "RESPONSIBILITIES:\n"
        "- Monitor delivery status and detect delays\n"
        "- Identify SLA breach risks for customer deliveries\n"
        "- Recommend rerouting options for delayed deliveries\n"
        "- Prioritize high-priority and premium customer deliveries\n\n"
        "AVAILABLE TOOLS:\n"
        "- detect_traffic_delays: Detect traffic delays and identify affected deliveries\n"
        "- reroute_delivery: Reroute a delivery to an alternative route\n"
        "- get_upcoming_deliveries: Get the upcoming deliveries and their status\n\n"
        "INSTRUCTIONS:\n"
        "- Use your tools to analyze delivery and traffic data\n"
        "- Identify deliveries at risk of SLA breaches\n"
        "- Provide specific rerouting recommendations with feasibility scores\n"
        "- Consider customer tier and penalties in prioritization\n"
        "- Respond with a concise summary of delivery status and corrective actions\n"
        "- Do NOT include raw data dumps in your response\n"
    ),
    name=AGENT_NAMES["distribution_handler"],
)

