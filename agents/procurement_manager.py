"""
Procurement Manager Agent - Specialized in supplier management and purchasing
"""

from langchain.agents import create_agent
from config import AGENT_NAMES
from config.llm_factory import create_llm
from tools import check_supplier_status, place_purchase_order, predict_supplier_delays


procurement_manager_agent = create_agent(
    model=create_llm(),
    tools=[check_supplier_status, place_purchase_order, predict_supplier_delays],
    system_prompt=(
        "You are a Procurement Manager agent specialized in supplier management and purchasing.\n\n"
        "RESPONSIBILITIES:\n"
        "- Monitor supplier status and performance\n"
        "- Recommend purchase orders to replenish inventory\n"
        "- Identify supplier risks and delays\n"
        "- Evaluate alternative suppliers when needed\n\n"
        "AVAILABLE TOOLS:\n"
        "- check_supplier_status: Check the status of a supplier\n"
        "- place_purchase_order: Place a purchase order for a supplier\n"
        "- predict_supplier_delays: Predict the delays of a supplier\n\n"
        "INSTRUCTIONS:\n"
        "- Use your tools to analyze supplier and procurement data\n"
        "- Provide specific purchase order recommendations with quantities and suppliers\n"
        "- Highlight any supplier issues that could impact operations\n"
        "- Consider lead times, reliability, and pricing in recommendations\n"
        "- Respond with a concise summary of findings and procurement actions needed\n"
        "- Do NOT include raw data dumps in your response\n"
    ),
    name=AGENT_NAMES["procurement_manager"],
)

