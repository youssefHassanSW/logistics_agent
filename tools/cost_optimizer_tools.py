"""
Cost Optimizer Agent Tools
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
def analyze_financial_costs(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Analyze all financial costs across operations to identify overruns and inefficiencies.
    Reads cost_analysis.csv to provide comprehensive cost breakdown.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        cost_path = scenario_path / "cost_analysis.csv"
        if not cost_path.exists():
            return "No cost analysis data available for this scenario"
        
        cost_df = pd.read_csv(cost_path)
        
        result = f"Financial Cost Analysis:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if 'actual_cost' in cost_df.columns:
            total_actual = cost_df['actual_cost'].sum()
            result += f"Total Actual Costs: ${total_actual:,.2f}\n"
        
        if 'budgeted_cost' in cost_df.columns:
            total_budget = cost_df['budgeted_cost'].sum()
            result += f"Total Budgeted Costs: ${total_budget:,.2f}\n"
            
            if 'actual_cost' in cost_df.columns:
                overrun = total_actual - total_budget
                overrun_pct = (overrun / total_budget * 100) if total_budget > 0 else 0
                
                if overrun > 0:
                    result += f"💰 Budget Overrun: ${overrun:,.2f} ({overrun_pct:+.1f}%)\n"
                else:
                    result += f"✓ Under Budget: ${abs(overrun):,.2f} ({overrun_pct:+.1f}%)\n"
        
        # Cost breakdown by category
        if 'category' in cost_df.columns:
            result += f"\n📊 Cost Breakdown by Category:\n"
            
            for _, cost_item in cost_df.iterrows():
                category = cost_item.get('category', 'N/A')
                actual = cost_item.get('actual_cost', 0)
                budgeted = cost_item.get('budgeted_cost', 0)
                
                result += f"\n{category}:\n"
                result += f"   Actual: ${actual:,.2f}\n"
                result += f"   Budget: ${budgeted:,.2f}\n"
                
                if budgeted > 0:
                    variance = ((actual - budgeted) / budgeted * 100)
                    if variance > 10:
                        status = "🚨 Over Budget"
                    elif variance > 5:
                        status = "⚠️ Slightly Over"
                    else:
                        status = "✓ On Track"
                    
                    result += f"   Variance: {variance:+.1f}% {status}\n"
                
                if 'potential_savings' in cost_item and cost_item['potential_savings'] > 0:
                    result += f"   💡 Potential Savings: ${cost_item['potential_savings']:,.2f}\n"
        
        # Total potential savings
        if 'potential_savings' in cost_df.columns:
            total_savings = cost_df['potential_savings'].sum()
            if total_savings > 0:
                result += f"\n💰 Total Potential Savings: ${total_savings:,.2f}\n"
        
        return result
        
    except Exception as e:
        return f"Error analyzing financial costs: {str(e)}"


@tool
def calculate_roi(
    scenario_dir: Annotated[str, "Scenario directory name"],
    investment_amount: Annotated[float, "Investment amount to calculate ROI for"],
    expected_savings: Annotated[float, "Expected monthly savings from investment"]
) -> str:
    """
    Calculate return on investment for cost optimization initiatives.
    Provides ROI analysis and payback period calculations.
    """
    try:
        # Calculate annual savings
        annual_savings = expected_savings * 12
        
        # Calculate ROI percentage
        roi_pct = ((annual_savings - investment_amount) / investment_amount * 100) if investment_amount > 0 else 0
        
        # Calculate payback period in months
        payback_months = (investment_amount / expected_savings) if expected_savings > 0 else float('inf')
        
        result = f"ROI Analysis:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Investment Amount: ${investment_amount:,.2f}\n"
        result += f"Expected Monthly Savings: ${expected_savings:,.2f}\n"
        result += f"Expected Annual Savings: ${annual_savings:,.2f}\n"
        result += f"\n📊 Financial Metrics:\n"
        result += f"   ROI (1 year): {roi_pct:+.1f}%\n"
        
        if payback_months != float('inf'):
            result += f"   Payback Period: {payback_months:.1f} months\n"
            
            if payback_months <= 6:
                assessment = "🟢 Excellent - Quick payback"
            elif payback_months <= 12:
                assessment = "🟡 Good - Reasonable payback"
            elif payback_months <= 24:
                assessment = "🟠 Fair - Long payback"
            else:
                assessment = "🔴 Poor - Very long payback"
            
            result += f"   Assessment: {assessment}\n"
        else:
            result += f"   Payback Period: Not achievable with current savings\n"
            result += f"   Assessment: 🔴 Not recommended\n"
        
        # 3-year projection
        three_year_savings = annual_savings * 3
        three_year_roi = ((three_year_savings - investment_amount) / investment_amount * 100) if investment_amount > 0 else 0
        
        result += f"\n📈 3-Year Projection:\n"
        result += f"   Total Savings: ${three_year_savings:,.2f}\n"
        result += f"   ROI: {three_year_roi:+.1f}%\n"
        
        return result
        
    except Exception as e:
        return f"Error calculating ROI: {str(e)}"


@tool
def identify_cost_savings(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Identify cost savings opportunities across routes, suppliers, and warehouse operations.
    Reads route_efficiency.csv, supplier_pricing.csv, and warehouse_utilization.csv.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        result = f"Cost Savings Opportunities:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        total_potential_savings = 0
        
        # Route efficiency analysis
        route_efficiency_path = scenario_path / "route_efficiency.csv"
        if route_efficiency_path.exists():
            route_df = pd.read_csv(route_efficiency_path)
            
            result += f"\n🚚 Route Optimization Opportunities:\n"
            result += f"   Routes analyzed: {len(route_df)}\n"
            
            if 'potential_savings' in route_df.columns:
                route_savings = route_df['potential_savings'].sum()
                total_potential_savings += route_savings
                result += f"   Potential savings: ${route_savings:,.2f}/month\n"
            
            if 'optimization_suggestion' in route_df.columns:
                suggestions = route_df[route_df['optimization_suggestion'].notna()]
                if not suggestions.empty:
                    result += f"\n   Top suggestions:\n"
                    for _, route in suggestions.head(3).iterrows():
                        result += f"   • Route {route.get('route_id', 'N/A')}: {route['optimization_suggestion']}"
                        if 'potential_savings' in route:
                            result += f" (Save: ${route['potential_savings']:.2f}/month)"
                        result += "\n"
        
        # Supplier pricing analysis
        supplier_pricing_path = scenario_path / "supplier_pricing.csv"
        if supplier_pricing_path.exists():
            supplier_df = pd.read_csv(supplier_pricing_path)
            
            result += f"\n💼 Supplier Cost Optimization:\n"
            result += f"   Suppliers compared: {len(supplier_df)}\n"
            
            if 'potential_savings' in supplier_df.columns:
                supplier_savings = supplier_df['potential_savings'].sum()
                total_potential_savings += supplier_savings
                result += f"   Potential savings: ${supplier_savings:,.2f}/month\n"
            
            # Find alternative suppliers with better pricing
            if 'savings_vs_current' in supplier_df.columns:
                better_options = supplier_df[supplier_df['savings_vs_current'] > 0]
                if not better_options.empty:
                    result += f"\n   Alternative suppliers with better pricing: {len(better_options)}\n"
                    for _, supplier in better_options.head(3).iterrows():
                        result += f"   • {supplier.get('supplier_name', 'N/A')}: "
                        result += f"Save ${supplier.get('savings_vs_current', 0):.2f}/month\n"
        
        # Warehouse utilization analysis
        warehouse_path = scenario_path / "warehouse_utilization.csv"
        if warehouse_path.exists():
            warehouse_df = pd.read_csv(warehouse_path)
            
            result += f"\n🏭 Warehouse Optimization:\n"
            result += f"   Warehouses analyzed: {len(warehouse_df)}\n"
            
            if 'utilization_pct' in warehouse_df.columns:
                avg_utilization = warehouse_df['utilization_pct'].mean()
                result += f"   Average utilization: {avg_utilization:.1f}%\n"
                
                # Identify under/over utilized warehouses
                underutilized = warehouse_df[warehouse_df['utilization_pct'] < 60]
                overutilized = warehouse_df[warehouse_df['utilization_pct'] > 90]
                
                if not underutilized.empty:
                    result += f"   ⚠️ Underutilized warehouses: {len(underutilized)}\n"
                
                if not overutilized.empty:
                    result += f"   ⚠️ Overutilized warehouses: {len(overutilized)}\n"
            
            if 'potential_savings' in warehouse_df.columns:
                warehouse_savings = warehouse_df['potential_savings'].sum()
                total_potential_savings += warehouse_savings
                result += f"   Potential savings: ${warehouse_savings:,.2f}/month\n"
        
        # Summary
        result += f"\n" + "="*40 + "\n"
        result += f"💰 TOTAL POTENTIAL SAVINGS: ${total_potential_savings:,.2f}/month\n"
        result += f"📅 Annual Savings Projection: ${total_potential_savings * 12:,.2f}\n"
        
        return result
        
    except Exception as e:
        return f"Error identifying cost savings: {str(e)}"

