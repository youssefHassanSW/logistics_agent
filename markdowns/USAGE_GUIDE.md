# Logistics Multi-Agent System - Usage Guide

## System Overview

The Logistics Multi-Agent System uses a supervisor/worker architecture where a Main Orchestrator coordinates 6 specialized agents to handle complex logistics scenarios.

### Architecture

```
Main Orchestrator (Supervisor)
    ├── Route Planner
    ├── Procurement Manager
    ├── Inventory Manager
    ├── Distribution Handler
    ├── Demand Forecaster
    └── Cost Optimizer
```

## Setup Instructions

### 1. Environment Setup

Activate the ML conda environment:
```bash
conda activate ML
```

### 2. API Key Configuration

Set your Anthropic API key:

**Windows (PowerShell/CMD):**
```bash
set ANTHROPIC_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Verify Installation

Run the structure tests to ensure everything is working:
```bash
python test_graph_structure.py
```

You should see all tests pass.

## Running Scenarios

### Interactive Mode (Recommended for First Use)

Simply run:
```bash
python main.py
```

This will:
1. List all available scenarios
2. Prompt you to select a scenario
3. Execute the scenario and display the results
4. Allow you to run multiple scenarios in sequence

### Run Specific Scenario

To run a specific scenario directly:
```bash
python main.py 1    # Low Inventory Crisis
python main.py 2    # Route Disruption
python main.py 3    # Demand Spike Forecast
python main.py 4    # Cost Optimization Analysis
python main.py 5    # Supplier Crisis
python main.py 6    # Distribution Delays & SLA
```

### List Available Scenarios

To see all scenarios without running them:
```bash
python main.py list
```

## Scenario Descriptions

### Scenario 1: Low Inventory Crisis
- **Complexity**: MEDIUM
- **Severity**: HIGH
- **Agents Used**: Inventory Manager → Procurement Manager
- **Description**: 5 products below reorder point requiring immediate procurement

### Scenario 2: Route Disruption
- **Complexity**: MEDIUM
- **Severity**: CRITICAL
- **Agents Used**: Route Planner → Distribution Handler
- **Description**: Traffic incidents affecting multiple delivery routes

### Scenario 3: Demand Spike Forecast
- **Complexity**: HIGH
- **Severity**: HIGH
- **Agents Used**: Demand Forecaster → Inventory Manager → Procurement Manager
- **Description**: AI predicts 130-300% demand increases for 6 products

### Scenario 4: Cost Optimization Analysis
- **Complexity**: VERY HIGH
- **Severity**: MEDIUM
- **Agents Used**: Cost Optimizer → Route Planner → Procurement Manager → Distribution Handler
- **Description**: $36K potential monthly savings identified across operations

### Scenario 5: Supplier Crisis
- **Complexity**: HIGH
- **Severity**: CRITICAL
- **Agents Used**: Procurement Manager → Inventory Manager → Route Planner
- **Description**: 5 suppliers with critical issues, $191K revenue at risk

### Scenario 6: Distribution Delays & SLA
- **Complexity**: HIGH
- **Severity**: CRITICAL
- **Agents Used**: Distribution Handler → Route Planner → Cost Optimizer
- **Description**: 2 SLA breaches for premium customers, $10K penalties

## Understanding the Output

When you run a scenario, you'll see:

### 1. Scenario Information
- Scenario name and description
- Severity and complexity levels
- Trigger event details

### 2. Agent Execution
- Sequential agent invocations
- Progress indicators showing which agent is working

### 3. Final Summary
A natural language summary containing:
- **Issue Description**: What logistics problem occurred
- **Agent Actions**: What each consulted agent did
- **Recommendations**: Specific actions to take
- **Business Impact**: Quantified impact (costs, risks, etc.)

## Advanced Usage

### Generate Graph Visualization

Create a PNG visualization of the multi-agent graph:
```bash
python main.py viz
# or specify output filename
python main.py viz my_graph.png
```

### Programmatic Usage

You can also import and use the system in your own Python code:

```python
from main import create_logistics_graph, run_scenario
from scenario_loader import load_scenario

# Create the graph
graph = create_logistics_graph()

# Load a scenario
scenario = load_scenario(1)

# Run it
final_state = run_scenario(1, verbose=True)
```

## Key Features

### State Management
- **Full Context**: Supervisor sees complete message history
- **Isolated Workers**: Each worker only sees their delegated task
- **Filtered Outputs**: Tool messages (CSV data) excluded from supervisor state
- **Tool Visibility**: Supervisor sees what tools were called, not raw outputs

### Agent Coordination
- **Sequential Delegation**: Agents called one at a time for better control
- **Smart Routing**: Supervisor determines which agents to consult
- **Always Returns**: Workers always report back to supervisor
- **Context Aware**: Routing based on scenario type and previous responses

## Troubleshooting

### API Key Not Set
```
[ERROR] ANTHROPIC_API_KEY environment variable not set
```
**Solution**: Set the API key as shown in Setup Instructions

### Import Errors
If you see import errors:
```bash
# Verify you're in the ML environment
conda activate ML

# Run structure tests
python test_graph_structure.py
```

### Scenario Not Found
```
Error: Invalid scenario ID X
```
**Solution**: Use `python main.py list` to see valid scenario IDs (1-6)

### Unicode Encoding Errors (Windows)
The system has been configured to avoid Unicode characters that cause issues on Windows. If you still see encoding errors, ensure your terminal supports UTF-8.

## File Structure Reference

```
better_logistics_agent/
├── main.py                      # Entry point
├── orchestrator.py              # Supervisor agent
├── agents.py                    # Worker agents
├── state_utils.py              # Message filtering
├── scenario_loader.py          # Scenario loading
├── config.py                   # Configuration
├── test_graph_structure.py     # Structure tests
├── tools/                      # Agent tools
│   ├── route_planner_tools.py
│   ├── procurement_tools.py
│   ├── inventory_tools.py
│   ├── distribution_tools.py
│   ├── forecaster_tools.py
│   └── cost_optimizer_tools.py
└── mock_data/                  # Scenario data
    └── scenario_*/             # 6 scenario directories
```

## Performance Notes

- **Token Usage**: State filtering significantly reduces token consumption
- **Response Time**: Sequential agent calls may take 30-90 seconds per scenario
- **API Costs**: Each scenario involves multiple LLM calls (5-15 depending on complexity)

## Best Practices

1. **Start Simple**: Begin with Scenario 1 (Low Inventory) to understand the flow
2. **Review Scenarios**: Use `python main.py list` to understand available scenarios
3. **Monitor Costs**: Each scenario makes multiple API calls to Claude
4. **Test Structure**: Run `test_graph_structure.py` after any code changes
5. **Read Summaries**: The final summary provides actionable insights

## Next Steps

After familiarizing yourself with the system:

1. Try all 6 scenarios to see different agent interactions
2. Review the tool implementations in `tools/` directory
3. Examine agent prompts in `agents.py` to understand specializations
4. Visualize the graph: `python main.py viz`
5. Explore the mock data in `mock_data/` directories

## Support

For issues or questions:
1. Check this usage guide
2. Review `README_IMPLEMENTATION.md` for technical details
3. Run structure tests to verify setup
4. Examine the scenario data in `mock_data/`

