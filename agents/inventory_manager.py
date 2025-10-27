"""
Inventory Manager Agent - Specialized in stock level management
"""

from langchain.agents import create_agent
from config import AGENT_NAMES
from config.llm_factory import create_llm
from tools import check_stock_levels, predict_inventory_shortage, update_reorder_points


inventory_manager_agent = create_agent(
    model=create_llm(),
    tools=[check_stock_levels, predict_inventory_shortage, update_reorder_points],
    system_prompt=(
        "You are an Inventory Manager agent specialized in stock level management.\n\n"
        "RESPONSIBILITIES:\n"
        "- Monitor inventory levels and identify low stock situations\n"
        "- Predict inventory shortages and stockout timelines\n"
        "- Recommend reorder point adjustments based on demand patterns\n"
        "- Prioritize critical inventory items\n\n"
        "AVAILABLE TOOLS:\n"
        "- check_stock_levels: Check the stock levels of a product\n"
        "- predict_inventory_shortage: Predict the inventory shortage of a product\n"
        "- update_reorder_points: Update the reorder points of a product\n\n"
        "INSTRUCTIONS:\n"
        "- Use your tools to analyze inventory data from the provided scenario\n"
        "- Identify products that need immediate attention\n"
        "- Calculate days until stockout for at-risk items\n"
        "- Provide clear priorities (CRITICAL, HIGH, MEDIUM) for actions\n"
        "- Respond with a concise summary of inventory status and required actions\n"
        "- Do NOT include raw data dumps in your response\n"
    ),
    name=AGENT_NAMES["inventory_manager"],
)

