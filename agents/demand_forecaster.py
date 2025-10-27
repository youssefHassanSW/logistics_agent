"""
Demand Forecaster Agent - Specialized in demand prediction and trend analysis
"""

from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from config import MODEL_NAME, AGENT_NAMES
from tools import predict_demand_spike, get_demand_forecast, analyze_historical_trends


def create_llm():
    """Create a Claude LLM instance"""
    return ChatAnthropic(model=MODEL_NAME, temperature=0)


demand_forecaster_agent = create_agent(
    model=create_llm(),
    tools=[predict_demand_spike, get_demand_forecast, analyze_historical_trends],
    system_prompt=(
        "You are a Demand Forecaster agent specialized in demand prediction and trend analysis.\n\n"
        "RESPONSIBILITIES:\n"
        "- Predict demand spikes and increases for products\n"
        "- Analyze historical demand trends and patterns\n"
        "- Provide demand forecasts with confidence levels\n"
        "- Identify products requiring proactive inventory buildup\n\n"
        "INSTRUCTIONS:\n"
        "- Use your tools to analyze demand forecast and historical data\n"
        "- Highlight significant demand changes (>20% increase)\n"
        "- Include confidence levels in your predictions\n"
        "- Consider forecast horizon and seasonality\n"
        "- Respond with a concise summary of demand predictions and recommended inventory adjustments\n"
        "- Do NOT include raw data dumps in your response\n"
    ),
    name=AGENT_NAMES["demand_forecaster"],
)

