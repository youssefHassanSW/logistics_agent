# Logistics Agent Mock Data Documentation

This directory contains mock data organized by scenario to test the multi-agent logistics orchestration system. Each scenario is designed to trigger specific agents and workflows.

## Scenario Overview

### Scenario 1: Low Inventory Crisis
**Trigger Event**: Critical inventory levels detected  
**Agent Flow**: Main Orchestrator → Inventory Manager → Procurement Manager  
**Description**: Multiple products have fallen below reorder points, requiring immediate procurement action.

**Key Data Points**:
- 5 products below reorder point (P001, P002, P004, P007, P009)
- Products marked as HIGH or CRITICAL priority
- Supplier information available for immediate ordering
- Expected workflow:
  1. Orchestrator receives LOW_INVENTORY event
  2. Inventory Manager checks which products are low
  3. Procurement Manager evaluates suppliers and places orders

**Files**:
- `inventory.csv` - Current stock levels with low inventory items
- `suppliers.csv` - Available suppliers with lead times and pricing
- `products.csv` - Product details including criticality and demand
- `trigger_event.csv` - Event that initiates the workflow

---

### Scenario 2: Route Disruption
**Trigger Event**: Major traffic incidents affecting deliveries  
**Agent Flow**: Main Orchestrator → Route Planner → Distribution Handler  
**Description**: Multiple routes are blocked or delayed due to accidents, requiring rerouting and delivery adjustments.

**Key Data Points**:
- 3 routes affected (R001, R003, R006)
- Traffic incidents include accidents and road closures
- High-priority deliveries at risk of SLA breach
- Expected workflow:
  1. Orchestrator receives ROUTE_DISRUPTION event
  2. Route Planner identifies alternative routes
  3. Distribution Handler reassigns vehicles and updates ETAs
  4. Route Planner optimizes new routes

**Files**:
- `routes.csv` - Active routes with status (DELAYED, BLOCKED, REROUTE_NEEDED)
- `vehicles.csv` - Vehicle fleet with current locations and status
- `deliveries.csv` - Delivery orders with priority and time windows
- `traffic_data.csv` - Real-time traffic incidents and delays
- `trigger_event.csv` - Event that initiates the workflow

---

### Scenario 3: Demand Spike Forecast
**Trigger Event**: AI forecast predicts significant demand increases  
**Agent Flow**: Main Orchestrator → Inventory Forecaster → Inventory Manager → Procurement Manager  
**Description**: Forecasting models detect imminent demand spikes for multiple products, requiring proactive inventory buildup.

**Key Data Points**:
- 6 products with predicted demand spikes (P001, P002, P004, P006, P009, P010)
- Demand increases ranging from 130% to 300%
- Current inventory insufficient to meet projected demand
- Historical data shows upward trend
- Expected workflow:
  1. Orchestrator receives DEMAND_SPIKE event
  2. Inventory Forecaster provides detailed predictions
  3. Inventory Manager calculates required stock levels
  4. Procurement Manager places advanced orders

**Files**:
- `demand_forecast.csv` - AI-generated demand predictions with confidence levels
- `inventory.csv` - Current stock with days until stockout calculations
- `suppliers.csv` - Supplier capacity and lead times
- `historical_demand.csv` - Past demand trends showing spike pattern
- `trigger_event.csv` - Event that initiates the workflow

---

### Scenario 4: Cost Optimization Analysis
**Trigger Event**: Monthly cost overruns detected  
**Agent Flow**: Main Orchestrator → Cost Optimizer → Route Planner → Procurement Manager → Distribution Handler  
**Description**: Cost analysis reveals significant overruns in fuel, shipping, and warehousing with multiple optimization opportunities.

**Key Data Points**:
- Total potential savings: $36,037/month
- Major cost issues: Fuel (+13%), Supplier Shipping (+22.2%)
- Route consolidation opportunities
- Alternative supplier pricing available
- Warehouse utilization inefficiencies
- Expected workflow:
  1. Orchestrator receives COST_OVERRUN event
  2. Cost Optimizer analyzes all cost categories
  3. Route Planner evaluates route consolidation
  4. Procurement Manager reviews supplier alternatives
  5. Distribution Handler optimizes delivery schedules

**Files**:
- `cost_analysis.csv` - Detailed cost breakdown by category
- `route_efficiency.csv` - Route-by-route cost analysis with optimization suggestions
- `supplier_pricing.csv` - Current vs. alternative supplier pricing comparison
- `warehouse_utilization.csv` - Warehouse efficiency metrics
- `trigger_event.csv` - Event that initiates the workflow

---

### Scenario 5: Supplier Crisis
**Trigger Event**: Multiple critical supplier failures  
**Agent Flow**: Main Orchestrator → Procurement Manager → Inventory Manager → Route Planner  
**Description**: Several suppliers experiencing critical issues including bankruptcy, quality problems, and delays affecting high-revenue products.

**Key Data Points**:
- 5 suppliers with critical/delayed status
- Revenue at risk: $191,725
- Products with stockout risk in 5-7 days
- Alternative suppliers available but require onboarding
- Expected workflow:
  1. Orchestrator receives SUPPLIER_DISRUPTION event
  2. Procurement Manager assesses supplier issues
  3. Procurement Manager evaluates alternative suppliers
  4. Inventory Manager calculates stockout timeline
  5. Route Planner adjusts inbound logistics for alternative suppliers

**Files**:
- `suppliers.csv` - Current supplier status with issue types
- `purchase_orders.csv` - Affected POs with delivery status
- `alternative_suppliers.csv` - Backup suppliers with onboarding times
- `affected_products.csv` - Products at risk with stockout calculations
- `trigger_event.csv` - Event that initiates the workflow

---

### Scenario 6: Distribution Delays & SLA Breaches
**Trigger Event**: Multiple deliveries delayed with SLA violations  
**Agent Flow**: Main Orchestrator → Distribution Handler → Route Planner → Cost Optimizer  
**Description**: Traffic incidents causing cascading delivery delays with 2 SLA breaches for premium customers, potential penalties of $10,000.

**Key Data Points**:
- 5 delayed deliveries (D3001, D3002, D3003, D3007, D3008)
- 2 confirmed SLA breaches for premium customers
- Multiple traffic incidents (accidents, construction, weather)
- Alternative routes available for most affected deliveries
- Expected workflow:
  1. Orchestrator receives DISTRIBUTION_DELAY event
  2. Distribution Handler assesses delay impact and SLA risk
  3. Route Planner calculates alternative routes
  4. Distribution Handler reroutes vehicles
  5. Cost Optimizer evaluates penalty vs. expedited shipping costs

**Files**:
- `deliveries.csv` - Active deliveries with delay status and SLA breach indicators
- `traffic_incidents.csv` - Real-time traffic problems with severity and clearance times
- `active_routes.csv` - Vehicle positions and updated ETAs
- `customer_sla.csv` - Customer SLA requirements and performance metrics
- `alternative_routes.csv` - Rerouting options with feasibility scores
- `trigger_event.csv` - Event that initiates the workflow

---

## Data Usage Guidelines

### For Testing Agent Workflows:

1. **Input to Main Orchestrator**: Use `trigger_event.csv` from each scenario
2. **Agent Tool Calls**: Agents should query the relevant CSVs based on their role
3. **Expected Outputs**: Agents should return actionable recommendations

### CSV Structure Notes:

- All timestamps are in `YYYY-MM-DD HH:MM:SS` format
- Currency values are in USD
- Distances in kilometers
- Weights in kilograms
- Percentages as decimals (0.95 = 95%)

### Scenario Selection Guide:

- **Test Inventory Management**: Use Scenarios 1 or 3
- **Test Route Optimization**: Use Scenarios 2 or 6
- **Test Procurement**: Use Scenarios 1, 3, or 5
- **Test Cost Analysis**: Use Scenario 4
- **Test Multi-Agent Coordination**: Use Scenarios 4, 5, or 6
- **Test Crisis Response**: Use Scenarios 5 or 6

---

## Agent-to-Data Mapping

### Route Planner Agent
- Reads: routes.csv, vehicles.csv, traffic_data.csv, alternative_routes.csv
- Tools: optimize_routes, assign_vehicle_to_route, check_traffic_conditions

### Procurement Manager Agent
- Reads: suppliers.csv, purchase_orders.csv, alternative_suppliers.csv, products.csv
- Tools: check_supplier_status, place_purchase_order, predict_supplier_delays

### Inventory Manager Agent
- Reads: inventory.csv, products.csv
- Tools: check_stock_levels, predict_inventory_shortage, update_reorder_points

### Distribution Handler Agent
- Reads: deliveries.csv, routes.csv, traffic_incidents.csv, customer_sla.csv
- Tools: detect_traffic_delays, reroute_delivery, get_upcoming_deliveries

### Inventory Forecaster Agent
- Reads: demand_forecast.csv, historical_demand.csv, inventory.csv
- Tools: predict_demand_spike, get_demand_forecast, analyze_historical_trends

### Cost Optimizer Agent
- Reads: cost_analysis.csv, route_efficiency.csv, supplier_pricing.csv, warehouse_utilization.csv
- Tools: analyze_financial_costs, calculate_roi, identify_cost_savings, calculate_total_system_cost

---

## Testing Recommendations

1. **Single Agent Test**: Start with Scenario 1 (simplest flow)
2. **Multi-Agent Coordination**: Progress to Scenario 3 or 4
3. **Complex Crisis Management**: Test with Scenarios 5 and 6
4. **End-to-End Integration**: Run all scenarios sequentially

Each scenario can be modified by adjusting severity levels, quantities, or adding/removing affected items to create variations.

