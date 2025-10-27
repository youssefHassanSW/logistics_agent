# Logistics Multi-Agent System

A supervisor/worker multi-agent system built with LangGraph and Claude for handling complex logistics scenarios.

## Architecture

- **Supervisor**: Main Orchestrator agent that coordinates all worker agents
- **Worker Agents** (6 specialized agents):
  - Route Planner - Route optimization and traffic management
  - Procurement Manager - Supplier management and purchase orders
  - Inventory Manager - Stock level monitoring and shortage prediction
  - Distribution Handler - Delivery management and SLA monitoring
  - Demand Forecaster - Demand prediction and trend analysis
  - Cost Optimizer - Financial analysis and cost reduction

## Project Structure

```
better_logistics_agent/
├── config.py                 # Configuration and constants
├── main.py                   # Entry point and graph assembly
├── orchestrator.py           # Supervisor agent with handoff tools
├── agents.py                 # Worker agent definitions
├── state_utils.py           # Message filtering utilities
├── scenario_loader.py       # Scenario loading utilities
├── tools/                   # Agent tools directory
│   ├── __init__.py
│   ├── route_planner_tools.py
│   ├── procurement_tools.py
│   ├── inventory_tools.py
│   ├── distribution_tools.py
│   ├── forecaster_tools.py
│   └── cost_optimizer_tools.py
└── mock_data/              # Scenario data
    ├── scenario_1_low_inventory/
    ├── scenario_2_route_disruption/
    ├── scenario_3_demand_spike/
    ├── scenario_4_cost_optimization/
    ├── scenario_5_supplier_issues/
    └── scenario_6_distribution_delays/
```

## Setup

1. Activate the ML conda environment:
```bash
conda activate ML
```

2. Set your Anthropic API key:
```bash
# Windows
set ANTHROPIC_API_KEY=your-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-key-here
```

## Usage

### Interactive Mode (Default)
```bash
python main.py
```

### Run Specific Scenario
```bash
python main.py 1    # Run scenario 1 (Low Inventory)
python main.py 2    # Run scenario 2 (Route Disruption)
# ... etc
```

### List Available Scenarios
```bash
python main.py list
```

### Generate Graph Visualization
```bash
python main.py viz
python main.py viz output_graph.png
```

## Available Scenarios

1. **Low Inventory Crisis** - Critical inventory levels requiring immediate procurement
2. **Route Disruption** - Traffic incidents affecting deliveries
3. **Demand Spike Forecast** - AI predicts significant demand increases
4. **Cost Optimization Analysis** - Monthly cost overruns detected
5. **Supplier Crisis** - Multiple critical supplier failures
6. **Distribution Delays & SLA** - Deliveries delayed with SLA violations

## Key Features

### State Management
- Supervisor maintains full message history
- Worker agents only see delegated tasks (isolated context)
- Tool messages (raw CSV data) filtered to reduce token usage
- Supervisor sees tool calls but not the full outputs

### Handoff Tools
- Each worker agent has a dedicated handoff tool
- Supervisor delegates tasks one at a time
- Workers always return to supervisor when done

### Agent Coordination
- Sequential task delegation (no parallel calls)
- Context-aware routing based on scenario type
- Natural language summaries for management review

## Example Output

The system provides:
1. Analysis of the logistics issue
2. Actions taken by each consulted agent
3. Overall recommendations and next steps
4. Natural language summary suitable for management

## Technical Details

- **LLM**: Claude 3.5 Sonnet (Anthropic)
- **Framework**: LangGraph
- **State**: MessagesState with filtered tool outputs
- **Tools**: 18 specialized CSV reading tools across 6 agents
- **Architecture**: Supervisor/Worker with handoff-based routing

