"""
Demand Forecaster Agent Tools
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
def predict_demand_spike(
    scenario_dir: Annotated[str, "Scenario directory name"],
    product_id: Annotated[str, "Product ID to analyze"] = None
) -> str:
    """
    Predict demand spikes for products based on forecasting models.
    Reads demand_forecast.csv to identify products with predicted demand increases.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        forecast_path = scenario_path / "demand_forecast.csv"
        if not forecast_path.exists():
            return "No demand forecast data available for this scenario"
        
        forecast_df = pd.read_csv(forecast_path)
        
        if product_id:
            forecast_df = forecast_df[forecast_df['product_id'] == product_id]
            if forecast_df.empty:
                return f"No forecast data for product {product_id}"
        
        result = f"Demand Spike Predictions:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        # Identify significant spikes (e.g., >20% increase)
        if 'predicted_demand_change_pct' in forecast_df.columns:
            spikes = forecast_df[forecast_df['predicted_demand_change_pct'] > 20]
        elif 'demand_change_pct' in forecast_df.columns:
            spikes = forecast_df[forecast_df['demand_change_pct'] > 20]
        else:
            spikes = forecast_df
        
        if not spikes.empty:
            result += f"Products with significant demand increases: {len(spikes)}\n\n"
            
            for _, item in spikes.iterrows():
                product_id = item.get('product_id', 'N/A')
                result += f"📈 Product {product_id}:\n"
                
                if 'current_demand' in item:
                    result += f"   Current Demand: {item['current_demand']:.0f} units/day\n"
                
                if 'predicted_demand' in item:
                    result += f"   Predicted Demand: {item['predicted_demand']:.0f} units/day\n"
                
                change_pct = item.get('predicted_demand_change_pct', item.get('demand_change_pct', 0))
                if change_pct >= 100:
                    urgency = "🚨 CRITICAL"
                elif change_pct >= 50:
                    urgency = "⚠️ HIGH"
                else:
                    urgency = "⚡ MODERATE"
                
                result += f"   Increase: {change_pct:+.1f}% {urgency}\n"
                
                if 'confidence' in item:
                    result += f"   Confidence: {item['confidence']:.1%}\n"
                
                if 'spike_reason' in item:
                    result += f"   Reason: {item['spike_reason']}\n"
                
                if 'forecast_horizon_days' in item:
                    result += f"   Timeframe: {item['forecast_horizon_days']} days\n"
                
                result += "\n"
        else:
            result += "No significant demand spikes predicted\n"
        
        return result
        
    except Exception as e:
        return f"Error predicting demand spike: {str(e)}"


@tool
def get_demand_forecast(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Get comprehensive demand forecast for all products.
    Reads demand_forecast.csv to provide overall demand predictions.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        forecast_path = scenario_path / "demand_forecast.csv"
        if not forecast_path.exists():
            return "No demand forecast data available for this scenario"
        
        forecast_df = pd.read_csv(forecast_path)
        
        result = f"Demand Forecast Overview:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"Products tracked: {len(forecast_df)}\n"
        
        if 'predicted_demand' in forecast_df.columns:
            total_predicted = forecast_df['predicted_demand'].sum()
            result += f"Total predicted demand: {total_predicted:.0f} units\n"
        
        if 'current_demand' in forecast_df.columns:
            total_current = forecast_df['current_demand'].sum()
            result += f"Current demand: {total_current:.0f} units\n"
            
            if 'predicted_demand' in forecast_df.columns:
                overall_change = ((total_predicted - total_current) / total_current * 100)
                result += f"Overall demand change: {overall_change:+.1f}%\n"
        
        # Average confidence
        if 'confidence' in forecast_df.columns:
            avg_confidence = forecast_df['confidence'].mean()
            result += f"Average forecast confidence: {avg_confidence:.1%}\n"
        
        # Categories of change
        if 'predicted_demand_change_pct' in forecast_df.columns or 'demand_change_pct' in forecast_df.columns:
            change_col = 'predicted_demand_change_pct' if 'predicted_demand_change_pct' in forecast_df.columns else 'demand_change_pct'
            
            increasing = forecast_df[forecast_df[change_col] > 10]
            stable = forecast_df[(forecast_df[change_col] >= -10) & (forecast_df[change_col] <= 10)]
            decreasing = forecast_df[forecast_df[change_col] < -10]
            
            result += f"\n📊 Forecast Distribution:\n"
            result += f"   Increasing demand: {len(increasing)} products\n"
            result += f"   Stable demand: {len(stable)} products\n"
            result += f"   Decreasing demand: {len(decreasing)} products\n"
        
        # Top movers
        if 'predicted_demand_change_pct' in forecast_df.columns or 'demand_change_pct' in forecast_df.columns:
            change_col = 'predicted_demand_change_pct' if 'predicted_demand_change_pct' in forecast_df.columns else 'demand_change_pct'
            top_gainers = forecast_df.nlargest(5, change_col)
            
            result += f"\n🔝 Top 5 Demand Increases:\n"
            for _, item in top_gainers.iterrows():
                result += f"   • {item.get('product_id', 'N/A')}: {item[change_col]:+.1f}%\n"
        
        return result
        
    except Exception as e:
        return f"Error getting demand forecast: {str(e)}"


@tool
def analyze_historical_trends(scenario_dir: Annotated[str, "Scenario directory name"]) -> str:
    """
    Analyze historical demand trends to understand patterns and seasonality.
    Reads historical_demand.csv to identify demand patterns.
    """
    scenario_path = _get_scenario_path(scenario_dir)
    
    try:
        historical_path = scenario_path / "historical_demand.csv"
        if not historical_path.exists():
            return "No historical demand data available for this scenario"
        
        historical_df = pd.read_csv(historical_path)
        
        result = f"Historical Demand Trend Analysis:\n"
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if 'date' in historical_df.columns:
            result += f"Data points: {len(historical_df)}\n"
            result += f"Period: {historical_df['date'].min()} to {historical_df['date'].max()}\n"
        
        # Analyze trends by product
        if 'product_id' in historical_df.columns:
            products = historical_df['product_id'].unique()
            result += f"Products tracked: {len(products)}\n\n"
            
            for product in products[:10]:  # Limit to first 10 products
                product_data = historical_df[historical_df['product_id'] == product]
                
                if 'demand' in product_data.columns and len(product_data) > 1:
                    result += f"📊 Product {product}:\n"
                    
                    # Calculate trend
                    first_demand = product_data['demand'].iloc[0]
                    last_demand = product_data['demand'].iloc[-1]
                    avg_demand = product_data['demand'].mean()
                    
                    if first_demand > 0:
                        trend = ((last_demand - first_demand) / first_demand * 100)
                        if trend > 10:
                            trend_indicator = "📈 Upward"
                        elif trend < -10:
                            trend_indicator = "📉 Downward"
                        else:
                            trend_indicator = "➡️ Stable"
                        
                        result += f"   Trend: {trend_indicator} ({trend:+.1f}%)\n"
                    
                    result += f"   Average Demand: {avg_demand:.1f} units\n"
                    
                    # Volatility
                    if len(product_data) > 2:
                        volatility = product_data['demand'].std()
                        result += f"   Volatility (std dev): {volatility:.1f}\n"
                    
                    result += "\n"
        else:
            # Aggregate analysis if no product breakdown
            if 'demand' in historical_df.columns:
                result += f"Total demand over period: {historical_df['demand'].sum():.0f}\n"
                result += f"Average demand: {historical_df['demand'].mean():.1f}\n"
        
        return result
        
    except Exception as e:
        return f"Error analyzing historical trends: {str(e)}"

