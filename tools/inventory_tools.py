"""
Inventory Manager Agent Tools
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
def check_stock_levels(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Check current inventory stock levels and identify products below reorder points.
    Reads inventory.csv to provide stock level analysis.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        inventory_df = pd.read_csv(scenario_path / "inventory.csv")
        
        result = f"Inventory Stock Level Analysis:\n"
        result += f"Total products tracked: {len(inventory_df)}\n"
        
        if 'current_stock' in inventory_df.columns:
            total_stock = inventory_df['current_stock'].sum()
            result += f"Total units in stock: {total_stock}\n"
        
        # Check for low stock items
        if 'current_stock' in inventory_df.columns and 'reorder_point' in inventory_df.columns:
            low_stock = inventory_df[inventory_df['current_stock'] <= inventory_df['reorder_point']]
            
            if not low_stock.empty:
                result += f"\n⚠️ Products below reorder point: {len(low_stock)}\n"
                result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                
                for _, item in low_stock.iterrows():
                    result += f"  • Product {item.get('product_id', 'N/A')}: "
                    result += f"Stock={item.get('current_stock', 0)}, "
                    result += f"Reorder Point={item.get('reorder_point', 0)}"
                    
                    if 'priority' in item:
                        result += f", Priority={item['priority']}"
                    
                    if 'days_until_stockout' in item:
                        result += f"\n    ⏱️ Days until stockout: {item['days_until_stockout']}"
                    
                    result += "\n"
            else:
                result += f"\n✓ All products above reorder point\n"
        
        # Stock value if available
        if 'current_stock' in inventory_df.columns and 'unit_value' in inventory_df.columns:
            total_value = (inventory_df['current_stock'] * inventory_df['unit_value']).sum()
            result += f"\nTotal inventory value: ${total_value:,.2f}\n"
        
        return result
        
    except Exception as e:
        return f"Error checking stock levels: {str(e)}"


@tool
def predict_inventory_shortage(
    scenario_dir: Annotated[str, "Scenario directory name"],
    product_id: Annotated[str, "Product ID to analyze"] = None
) -> str:
    """
    Predict inventory shortages and calculate days until stockout.
    Analyzes inventory.csv and products.csv to forecast shortage timeline.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        inventory_df = pd.read_csv(scenario_path / "inventory.csv")
        
        if product_id:
            inventory_df = inventory_df[inventory_df['product_id'] == product_id]
            if inventory_df.empty:
                return f"Product {product_id} not found in inventory"
        
        result = f"Inventory Shortage Prediction:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Identify products at risk
        at_risk = pd.DataFrame()
        if 'days_until_stockout' in inventory_df.columns:
            at_risk = inventory_df[inventory_df['days_until_stockout'] <= 14]
        elif 'current_stock' in inventory_df.columns and 'reorder_point' in inventory_df.columns:
            at_risk = inventory_df[inventory_df['current_stock'] <= inventory_df['reorder_point']]
        
        if not at_risk.empty:
            result += f"Products at risk of shortage: {len(at_risk)}\n\n"
            
            for _, item in at_risk.iterrows():
                result += f"📦 Product {item.get('product_id', 'N/A')}:\n"
                result += f"   Current Stock: {item.get('current_stock', 0)}\n"
                
                if 'reorder_point' in item:
                    result += f"   Reorder Point: {item.get('reorder_point', 0)}\n"
                
                if 'days_until_stockout' in item:
                    days = item['days_until_stockout']
                    if days <= 3:
                        urgency = "🚨 CRITICAL"
                    elif days <= 7:
                        urgency = "⚠️ HIGH"
                    else:
                        urgency = "⚡ MEDIUM"
                    result += f"   Days Until Stockout: {days} {urgency}\n"
                
                if 'daily_demand' in item:
                    result += f"   Daily Demand: {item['daily_demand']}\n"
                
                if 'priority' in item:
                    result += f"   Priority: {item['priority']}\n"
                
                result += "\n"
        else:
            result += "✓ No immediate shortage risks detected\n"
        
        return result
        
    except Exception as e:
        return f"Error predicting inventory shortage: {str(e)}"


@tool
def update_reorder_points(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Analyze and recommend updates to reorder points based on demand patterns.
    Reads products.csv and inventory.csv to optimize reorder points.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        inventory_df = pd.read_csv(scenario_path / "inventory.csv")
        
        # Try to load products.csv for additional context
        products_path = scenario_path / "products.csv"
        products_df = None
        if products_path.exists():
            products_df = pd.read_csv(products_path)
        
        result = f"Reorder Point Analysis:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        recommendations = []
        
        for _, item in inventory_df.iterrows():
            product_id = item.get('product_id', 'N/A')
            current_reorder = item.get('reorder_point', 0)
            current_stock = item.get('current_stock', 0)
            
            # Calculate recommended reorder point based on demand
            if 'daily_demand' in item:
                daily_demand = item['daily_demand']
                lead_time = item.get('lead_time_days', 7)  # Default 7 days
                safety_stock_days = 3  # 3 days safety stock
                
                recommended_reorder = daily_demand * (lead_time + safety_stock_days)
                
                if abs(recommended_reorder - current_reorder) > daily_demand:
                    change_pct = ((recommended_reorder - current_reorder) / current_reorder * 100) if current_reorder > 0 else 0
                    
                    recommendations.append({
                        'product_id': product_id,
                        'current': current_reorder,
                        'recommended': recommended_reorder,
                        'change_pct': change_pct,
                        'priority': item.get('priority', 'MEDIUM')
                    })
        
        if recommendations:
            result += f"Recommended Reorder Point Adjustments: {len(recommendations)}\n\n"
            
            for rec in sorted(recommendations, key=lambda x: abs(x['change_pct']), reverse=True)[:10]:
                result += f"📊 Product {rec['product_id']}:\n"
                result += f"   Current Reorder Point: {rec['current']:.0f}\n"
                result += f"   Recommended: {rec['recommended']:.0f}\n"
                result += f"   Change: {rec['change_pct']:+.1f}%\n"
                result += f"   Priority: {rec['priority']}\n\n"
        else:
            result += "✓ Current reorder points are appropriately set\n"
        
        return result
        
    except Exception as e:
        return f"Error updating reorder points: {str(e)}"

