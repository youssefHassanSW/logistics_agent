"""
Procurement Manager Agent Tools
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
def check_supplier_status(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Check the status of all suppliers including availability, lead times, and any issues.
    Reads suppliers.csv to provide supplier status overview.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        suppliers_df = pd.read_csv(scenario_path / "suppliers.csv")
        
        result = f"Supplier Status Analysis:\n"
        result += f"Total suppliers: {len(suppliers_df)}\n"
        
        if 'status' in suppliers_df.columns:
            status_counts = suppliers_df['status'].value_counts()
            result += f"\nSupplier Status Distribution:\n{status_counts.to_string()}\n"
            
            # Identify problematic suppliers
            problem_statuses = ['CRITICAL', 'DELAYED', 'QUALITY_ISSUE', 'BANKRUPTCY']
            problem_suppliers = suppliers_df[suppliers_df['status'].isin(problem_statuses)]
            
            if not problem_suppliers.empty:
                result += f"\n⚠️ Suppliers with issues: {len(problem_suppliers)}\n"
                for _, supplier in problem_suppliers.iterrows():
                    result += f"  - {supplier.get('supplier_name', 'N/A')} (ID: {supplier.get('supplier_id', 'N/A')}): "
                    result += f"{supplier.get('status', 'N/A')}"
                    if 'issue_type' in supplier:
                        result += f" - {supplier['issue_type']}"
                    result += "\n"
        
        # Average lead time
        if 'lead_time_days' in suppliers_df.columns:
            avg_lead_time = suppliers_df['lead_time_days'].mean()
            result += f"\nAverage lead time: {avg_lead_time:.1f} days\n"
        
        # Reliability info
        if 'reliability_score' in suppliers_df.columns:
            avg_reliability = suppliers_df['reliability_score'].mean()
            result += f"Average reliability score: {avg_reliability:.2f}\n"
        
        return result
        
    except Exception as e:
        return f"Error checking supplier status: {str(e)}"


@tool
def place_purchase_order(
    scenario_dir: Annotated[str, "Scenario directory name"],
    supplier_id: Annotated[str, "Supplier ID to place order with"],
    product_id: Annotated[str, "Product ID to order"],
    quantity: Annotated[int, "Quantity to order"]
) -> str:
    """
    Create a purchase order recommendation with a specific supplier for a product.
    Analyzes supplier data to provide ordering recommendations.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        suppliers_df = pd.read_csv(scenario_path / "suppliers.csv")
        
        # Find the supplier
        supplier = suppliers_df[suppliers_df['supplier_id'] == supplier_id]
        if supplier.empty:
            return f"Supplier {supplier_id} not found"
        
        supplier_info = supplier.iloc[0]
        
        # Check if products.csv exists for product info
        products_path = scenario_path / "products.csv"
        product_name = product_id
        if products_path.exists():
            products_df = pd.read_csv(products_path)
            product = products_df[products_df['product_id'] == product_id]
            if not product.empty:
                product_name = product.iloc[0].get('product_name', product_id)
        
        result = f"Purchase Order Recommendation:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Supplier: {supplier_info.get('supplier_name', 'N/A')} (ID: {supplier_id})\n"
        result += f"Status: {supplier_info.get('status', 'N/A')}\n"
        result += f"Product: {product_name}\n"
        result += f"Quantity: {quantity}\n"
        
        if 'unit_price' in supplier_info:
            total_cost = supplier_info['unit_price'] * quantity
            result += f"Unit Price: ${supplier_info['unit_price']:.2f}\n"
            result += f"Total Cost: ${total_cost:.2f}\n"
        
        if 'lead_time_days' in supplier_info:
            result += f"Expected Lead Time: {supplier_info['lead_time_days']} days\n"
        
        if 'reliability_score' in supplier_info:
            result += f"Supplier Reliability: {supplier_info['reliability_score']:.2f}\n"
        
        # Warning if supplier has issues
        if supplier_info.get('status') not in ['ACTIVE', 'OPERATIONAL']:
            result += f"\n⚠️ WARNING: Supplier status is {supplier_info.get('status')}. Consider alternative suppliers.\n"
        
        return result
        
    except Exception as e:
        return f"Error creating purchase order: {str(e)}"


@tool
def predict_supplier_delays(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Predict potential supplier delays by analyzing purchase orders and supplier performance.
    Reads purchase_orders.csv to identify at-risk orders.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        po_path = scenario_path / "purchase_orders.csv"
        if not po_path.exists():
            return "No purchase orders data available for this scenario"
        
        po_df = pd.read_csv(po_path)
        
        result = f"Supplier Delay Prediction Analysis:\n"
        result += f"Total purchase orders: {len(po_df)}\n"
        
        if 'status' in po_df.columns:
            status_counts = po_df['status'].value_counts()
            result += f"\nPO Status Distribution:\n{status_counts.to_string()}\n"
            
            # Identify delayed or at-risk orders
            problem_statuses = ['DELAYED', 'AT_RISK', 'CRITICAL']
            problem_pos = po_df[po_df['status'].isin(problem_statuses)]
            
            if not problem_pos.empty:
                result += f"\n⚠️ Orders at risk: {len(problem_pos)}\n"
                for _, po in problem_pos.head(10).iterrows():
                    result += f"  - PO {po.get('po_id', 'N/A')}: {po.get('product_id', 'N/A')} "
                    result += f"from {po.get('supplier_id', 'N/A')} - {po.get('status', 'N/A')}"
                    if 'expected_delivery' in po:
                        result += f" (Expected: {po['expected_delivery']})"
                    result += "\n"
        
        # Calculate delay impact
        if 'quantity' in po_df.columns and 'status' in po_df.columns:
            delayed_qty = po_df[po_df['status'].isin(['DELAYED', 'AT_RISK'])]['quantity'].sum()
            result += f"\nTotal quantity at risk of delay: {delayed_qty}\n"
        
        return result
        
    except Exception as e:
        return f"Error predicting supplier delays: {str(e)}"

